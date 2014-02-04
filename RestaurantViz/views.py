from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from fsmodel import getExploreRestaurants
from django.utils import simplejson

def restVizApp(request):
    #renders a html with data from fsmodel.getExploreRestaurants
    #currently hard coded for Xian's Famous Foods
    t = get_template('RestViz.html')
    restID = '4c2a81398abca59393c8fe1f'
    #restID = '4b3a3bc8f964a520b06225e3'

    resultList = getExploreRestaurants(restID)
    #note that when using the json dump you will need to open it as safe
    #example {{js_data|safe}}
    js_data = simplejson.dumps(resultList[0])
    js_resultList = simplejson.dumps(resultList[1])
    html = t.render(Context({'seedName' : js_data, 'resultList' : js_resultList}))
    return HttpResponse(html)
