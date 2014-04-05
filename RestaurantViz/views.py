from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.template.loader import get_template
from fsmodel import searchFS, restRanker
import django.utils.simplejson as json

def restVizApp(request):
    #renders a html with data from fsmodel.getExploreRestaurants
    #currently hard coded for Xian's Famous Foods
    
    if request.POST.has_key('user_location'):
        vizHelper = restRanker()
        vizHelper.updateLocation(request.POST['user_location'])
        vizHelper.seedRestFSID = request.POST['seedID']
        jsData = getUpdate(vizHelper)
        return HttpResponse(jsData)

    if request.POST.has_key('restSearch'):
        vizHelper = restRanker()
        sessionSearch = searchFS()
        sessionSearch.searchQuery =request.POST['restSearch']
        sessionSearch.searchLoc = request.POST['restSearchLoc']
        searchData = sessionSearch.getRestSearch()
        jsData = json.dumps({'searchResults' : searchData})
        return HttpResponse(jsData)

    if request.POST.has_key('updateRest'):
        vizHelper = restRanker()
        print request.POST  
        vizHelper.seedRestFSID = request.POST['updateRest']
        vizHelper.updateLocation(request.POST['userLoc'])
        jsData = getUpdate(vizHelper)
        return HttpResponse(jsData)

    vizHelper = restRanker()
    t = get_template('RestViz.html')
    jsData = get_initData(vizHelper)
    #print jsData
    c = RequestContext(request, jsData)
    html = t.render(c)
    
    return HttpResponse(html)

def get_initData(vizHelper):
    #note that when using the json dump you will need to open it as safe
    #example {{js_data|safe}}
    resultList = vizHelper.getRankedRestaurants()
    js_data = json.dumps(resultList[0])
    js_fsid = json.dumps(vizHelper.seedRestFSID)
    js_resultList = json.dumps(resultList[1])
    js_loc = json.dumps(vizHelper.locationDict)
    return {'seedName' : js_data, 'seedID' :js_fsid, 'resultList' : js_resultList, 'location' : js_loc}

def getUpdate(vizHelper):
    #note that when using the json dump you will need to open it as safe
    #example {{js_data|safe}}
    resultList = vizHelper.getRankedRestaurants()
    return json.dumps({'seedName' : resultList[0], 'seedID' : vizHelper.seedRestFSID, 'resultList' : resultList[1], 'location' : vizHelper.locationDict})

def testhtml(request):
    return render_to_response('test.html', context_instance=RequestContext(request))

