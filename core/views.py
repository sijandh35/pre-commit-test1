from django.shortcuts import render,redirect
from .models import Project,Category
# Create your views here.
from django.db.models import Count,Q,Sum,Max
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import datetime
from notification.tasks import sum
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
import json

CACHE_TTL = getattr(settings,'CACHE_TTL', DEFAULT_TIMEOUT)


def redis_test(value):
    json1 = json.dumps({ "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
      "properties": {"prop0": "value0"}
      },
    { "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
          ]
        },
      "properties": {
        "prop0": "value0",
        "prop1": 0.0
        }
      },
    { "type": "Feature",
       "geometry": {
         "type": "Polygon",
         "coordinates": [
           [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
             [100.0, 1.0], [100.0, 0.0] ]
           ]
       },
       "properties": {
         "prop0": "value0",
         "prop1": {"this": "that"}
         }
       }
    ]
  })
    
    if cache.get(value):
        data = 'From Redis value is {}'.format(json1)
    else:
        cache.set(value, json1)
        data = f'SET DATA TO REDIS {json1}'
    return data

@login_required(login_url='/login')
def index(request):
    # data = Category.objects.get(id=1)
    # print(Category.objects.select_related('project_category').prefetch_related('many_category').values('many_category__name'))
    # data1 = Project.objects.select_related('category')
    # print("PREFETCH RELATED")
    # print(vars(data[0]))
    # print("SELECT RELATED")
    # print(vars(data1[0]))
    # print(request.COOKIES)
    obj  = Session.objects.get(session_key=request.COOKIES['sessionid'])
    session_data = obj.get_decoded()
    
    response  = render(request,'index.html',{'redis_status':redis_test(request.GET.get('value'))})
    response.set_cookie('last_connection', datetime.datetime.now())
    response.set_cookie('username', datetime.datetime.now())
    response.delete_cookie('username')
    print(request.COOKIES.get('username'))
    # print(sum.delay(5,6))
    # print(session_data)
    return response

def loginview(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('/')
        
        else:
            return render(request,'login.html')      
        
        
def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/login')  
        