import foursquare
import random
from math import *

def main():
    restID = '4c2a81398abca59393c8fe1f'
    restID = '4b3a3bc8f964a520b06225e3'
    getExploreRestaurants(restID)

def getExploreRestaurants(restID):
    client = getFSClient()
    seedRest = client.venues(restID)['venue']
    seedLat = seedRest['location']['lat']
    seedLng = seedRest['location']['lng']
    try:
        seedPrice = seedRest['price']['tier']
    except:
        seedPrice = -1
    seedTags = seedRest['tags']
    seedCat = seedRest['categories'][0]['name']

    exploreParams = {
        'll' :'40.73,-73.98',
        'radius' : 1000,
        'limit' : 10,
        'section' : '',
        'query' : ''
        }

    resultList = {}
    if seedTags == [] :
        seedTags=[seedCat]
    for tag in seedTags:
        exploreParams['query'] = tag
        possibleVenues= client.venues.explore(params=exploreParams)

        countme = 1
        for x in possibleVenues['groups'][0]['items']:
            tempID = x['venue']['id']
            if x['venue']['id'] not in resultList.keys()+[restID]:
                resultList[tempID] = x['venue']
                resultList[tempID]['rvScore'] = 1
            else:
                if tempID <> restID:
                    resultList[tempID]['rvScore']= resultList[tempID]['rvScore'] + 1 
            countme = countme + 1
        print ''

    countme = 1
    tinyResult = []
    maxScore = 0
    
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
        resultList[x]['rvDistance'] = distanceLL(seedLng, seedLat, targetLon, targetLat)
        resultList[x]['rvDistScore'] = distanceScore(resultList[x]['rvDistance'])
        countme = countme + 1
        resultList[x]['rvTotalScore'] = resultList[x]['rvPriceScore'] + resultList[x]['rvScore'] *5 + resultList[x]['rvDistScore']
        tempDict = {
            'name' : resultList[x]['name'],
            'priceScore' : resultList[x]['rvPriceScore'],
            'distScore' : resultList[x]['rvDistScore'],
            'catScore' : resultList[x]['rvScore'],
            'totalScore' : resultList[x]['rvTotalScore']}

        insertIndex = 0
        insertTF = False
        while insertIndex < len(tinyResult) and insertTF == False:
            if resultList[x]['rvTotalScore'] < tinyResult[insertIndex]['totalScore']:
                insertIndex = insertIndex + 1
            else:
                insertTF = True

        tinyResult.insert(insertIndex, tempDict)

    #simple
    if len(tinyResult) > 10:
        tinyResult = tinyResult[:10]
        
    random.shuffle(tinyResult)
    return [seedRest['name'], tinyResult]

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
    clientID = '5UAC11MZ4H4TRPKPIBFXSSU0BLFWUJDK1VVERD3HMEARU1BF'
    clientCode = 'VBX3IFJNEH4FFPL3JBR3BTAHGTTMHZVTUQHBQKIZBSNYW2MX'
    client = foursquare.Foursquare(client_id=clientID, client_secret=clientCode, redirect_uri='http://fondu.com/oauth/authorize')
    auth_uri = client.oauth.auth_url()
    return client

    
if __name__ == '__main__' :
    main()
