import foursquare
import random
from math import *
from geopy import geocoders

class restRanker():
    def __init__(self):
        self.FSClient = getFSClient()
        self.seedRestFSID = '4c2a81398abca59393c8fe1f'
        self.location = "NYC"
        self.geoCoder = geocoders.GoogleV3()
        self.updateLocation(self.location)
        
    def updateLocation(self, loc):
        output = {}
        g = geocoders.GoogleV3()
        place, (lat, lng) = self.geoCoder.geocode(loc)
        output['address'] = place
        output['lat'] = lat
        output['lng'] = lng
        output['ll'] = str(lat) + ',' + str(lng)

        self.location = loc
        self.locationDict = output

    def getLocationDict(self):
        return self.locationDict
        

    def getRankedRestaurants(self):
        #builds results, location needs to be made dynamic
        seedRest = self.FSClient.venues(self.seedRestFSID)['venue']
        try:
            seedPrice = seedRest['price']['tier']
        except:
            seedPrice = -1
        seedTags = seedRest['tags']
        seedCat = seedRest['categories'][0]['name']

        #defines paramters for the explore query
        exploreParams = {
            'll' : self.locationDict['ll'],
            'radius' : 1000,
            'limit' : 10,
            'section' : '',
            'query' : ''
            }

        #builds a unique list of results from iterating over tags and querying fs
        resultList = {}
        if seedTags == [] :
            seedTags=[seedCat]
        for tag in seedTags:
            exploreParams['query'] = tag
            possibleVenues= self.FSClient.venues.explore(params=exploreParams)

            countme = 1
            for x in possibleVenues['groups'][0]['items']:
                tempID = x['venue']['id']
                if x['venue']['id'] not in resultList.keys()+[self.seedRestFSID]:
                    resultList[tempID] = x['venue']
                    resultList[tempID]['rvScore'] = 1
                else:
                    if tempID <> self.seedRestFSID:
                        resultList[tempID]['rvScore']= resultList[tempID]['rvScore'] + 1 
                countme = countme + 1
            print ''

        countme = 1
        tinyResult = []
        maxScore = 0

        #Scores results and makes a smaller list of scores and venue name
        #new list is ordered by total score
        for x in resultList.keys():
            tempDict= {}
            targetLat = resultList[x]['location']['lat']
            targetLon = resultList[x]['location']['lng']
            try:
                targetPrice = resultList[x]['price']['tier']
            except:
                targetPrice = -1
            if targetPrice <> -1 and seedPrice <> -1:
                resultList[x]['rvPriceScore'] = 3- abs(seedPrice-targetPrice)
            else:
                resultList[x]['rvPriceScore'] = 1
            resultList[x]['rvDistance'] = distanceLL(self.locationDict['lng'], self.locationDict['lat'], targetLon, targetLat)
            resultList[x]['rvDistScore'] = distanceScore(resultList[x]['rvDistance'])
            countme = countme + 1
            resultList[x]['rvTotalScore'] = resultList[x]['rvPriceScore'] + resultList[x]['rvScore'] *5 + resultList[x]['rvDistScore']
            tempDict = {
                'name' : resultList[x]['name'],
                'priceScore' : resultList[x]['rvPriceScore'],
                'distScore' : resultList[x]['rvDistScore'],
                'phraseScore' : resultList[x]['rvScore'],
                'totalScore' : resultList[x]['rvTotalScore']}

            insertIndex = 0
            insertTF = False
            while insertIndex < len(tinyResult) and insertTF == False:
                if resultList[x]['rvTotalScore'] < tinyResult[insertIndex]['totalScore']:
                    insertIndex = insertIndex + 1
                else:
                    insertTF = True

            tinyResult.insert(insertIndex, tempDict)

        #limits the results to the top 10 as per score and shuffles
        if len(tinyResult) > 10:
            tinyResult = tinyResult[:10]       
        random.shuffle(tinyResult)
        
        return [seedRest['name'], tinyResult]

class searchFS():
    def __init__(self):
        self.FSClient = getFSClient()
        self.searchQuery = "Xian"
        self.searchLoc = "NYC"
        
    def getRestSearch(self):
        output = []
        params = {  'query' : self.searchQuery, 'near' : self.searchLoc,
                'categoryId' : '4d4b7105d754a06374d81259'}
        searchResults = self.FSClient.venues.search(params)
        for res in searchResults['venues']:
            try:
                venAddress = res['location']['address']
            except:
                venAddress = "NO ADDRESS"
            try:
                venName = res['name']
            except:
                venName = "MISSING NAME"
            output.append({'name' : venName, 'address' : venAddress, 'idFS' : res['id']})
        return output

def distanceLL(lon1, lat1, lon2, lat2):
    #Implements Haversine formula using miles
    radLon1 = radians(lon1)
    radLat1 = radians(lat1)
    radLon2 = radians(lon2)
    radLat2 = radians(lat2)

    dlon = radLon2 - radLon1
    dlat = radLat2 - radLat1
    a = sin(dlat/2)**2 + cos(radLat1) * cos(radLat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return 3961 * c
    
def distanceScore(distance):
    #creates a bucketed score based on distance
    if distance < 0.25:
        output = 5
    elif distance < 0.5:
        output = 4
    elif distance < 1:
        output = 3
    elif distance < 2:
        output = 2
    else:
        output = 1

    return output


def getFSClient():
    #gets a foursquare client need to store the token better
    clientID = '5UAC11MZ4H4TRPKPIBFXSSU0BLFWUJDK1VVERD3HMEARU1BF'
    clientCode = 'VBX3IFJNEH4FFPL3JBR3BTAHGTTMHZVTUQHBQKIZBSNYW2MX'
    client = foursquare.Foursquare(client_id=clientID, client_secret=clientCode, redirect_uri='http://fondu.com/oauth/authorize')
    auth_uri = client.oauth.auth_url()
    return client

