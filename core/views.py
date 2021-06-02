from django.shortcuts import render,redirect
from .models import Project,Category
# Create your views here.
from django.db.models import Count,Q,Sum,Max
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import datetime


@login_required(login_url='/login')
def index(request):
    data = Category.objects.prefetch_related('project_category')
    data1 = Project.objects.select_related('category')
    # print("PREFETCH RELATED")
    # print(vars(data[0]))
    # print("SELECT RELATED")
    # print(vars(data1[0]))
    # print(request.COOKIES)
    obj  = Session.objects.get(session_key=request.COOKIES['sessionid'])
    session_data = obj.get_decoded()
    response  = render(request,'index.html')
    response.set_cookie('last_connection', datetime.datetime.now())
    response.set_cookie('username', datetime.datetime.now())
    response.delete_cookie('username')
    print(request.COOKIES.get('username'))
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
        