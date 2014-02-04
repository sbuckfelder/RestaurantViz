from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from fsmodel import getExploreRestaurants
from django.utils import simplejson

def dummyTest(request):
    t = get_template('dummy.html')
    restID = '4c2a81398abca59393c8fe1f'
    #restID = '4b3a3bc8f964a520b06225e3'


    resultList = getExploreRestaurants(restID)
    js_data = simplejson.dumps(resultList[0])
    js_resultList = simplejson.dumps(resultList[1])
    html = t.render(Context({'seedName' : js_data, 'resultList' : js_resultList}))
    return HttpResponse(html)
