from multiprocessing import context
import pdb
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib import messages
from django_application.tasks import send_email_task
from .models import Car,BuyCar,User,CarImage,Apicall
from .forms import CarForm,UserForm,BuyForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.core.mail import send_mail
from django.core .mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import json
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
import requests
import json


def home(request):
    return render(request,'home.html')
def base(request):
    return render(request,'base.html') 
def thankyou(request):
    return render(request,'thankyou.html') 
def success(request):
    return render(request,"success.html")

def carlist(request):     
    form = CarForm 
    if 'save' in request.POST :
        data = CarForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        print(data,"----")
        if data.is_valid():
            Car = data.save()
            for i in images:
                CarImage(Car=Car,image=i).save()
              
            return redirect('django_application:thankyou')
    return render(request,'carlist.html',{'form':form})   

def findcar(request):     
    data = Car.objects.all().order_by('-id')
    searchdata = request.GET.get('search')
    if searchdata is not None:  
        data = data.filter(Q(make__icontains = searchdata) | Q(year__icontains = searchdata)).distinct()                       
    paginator = Paginator(data,5) 
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    context = {
        'data' : data
    }
    return render(request,'findcar.html',context)

def signup(request):
    if request.method == 'POST':
        form  = UserForm(request.POST, request.FILES)
        if form.is_valid():    
            form.save()  
            messages.success(request,"successfully Registered !!!")  
            return redirect("django_application:login")
        else:
            return render(request,"signup.html",{'form':form})  
    else:
        form = UserForm(request.POST)
        return render(request,"signup.html",{'form':form}) 

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request,user)
                messages.success(request,"Successfully login to Home page !!")
                return redirect('django_application:home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('django_application:login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('django_application:login')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})  

def logout(request):
    django_logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('django_application:base')

def buycardetail(request,id):
    data = Car.objects.filter(id=id).first()
    data1 = CarImage.objects.all() 
    context = {
        'data' : data,
        'id' : id,
        'data1':data1,
    } 
    return render(request,"buycardetail.html",context)  
    
def cardetail(request,id):
        data = Car.objects.filter(id=id).first()    
        context = {
            'data': data,    
            'id': id,
        }    
        return render(request, "cardetail.html", context)
          
def buycar(request,id):
    cardata = Car.objects.filter(id=id).first()
    if request.method == 'POST':
            form = BuyForm(request.POST,request.FILES)
            if form.is_valid():
                buyername = form.cleaned_data.get('buyer_name')
                buyernumber = form.cleaned_data.get('buyer_number')
                buycarobj = BuyCar(Car=cardata,buyer_name= buyername,buyer_number=buyernumber)
                buycarobj.save()
                email = request.user.email
                send_email_task.delay(buycarobj.id,email)   
                return redirect("django_application:success")       
            else:    
                return render(request,"buycar.html",{'form':form,'cardata':cardata})                
    cardata.status = 'sold'
    cardata.save()
    form = BuyForm(request.POST)
    return render(request,"buycar.html",{'form':form,'cardata':cardata}) 

# def schedule_mail(request):
#     schedule, created = CrontabSchedule.objects.get_or_create(hour=0, minute=1)
#     task = PeriodicTask.objects.create(
#         crontab=schedule,
#         name="schedule_mail_task_" + "5",
#         task="send_mail_app.tasks.send_mail_func",
#     )  # , args = json.dumps([[2,3]]))
#     return HttpResponse("Done")

def carstatus(request):   
    context = {}
    if request.user.is_superuser: 
        cardata = Car.objects.filter(status = 'sold') 
        context = {
            'cardata': cardata,
        }
    elif request.user.is_authenticated:
        cardata = Car.objects.exclude(status = 'sold')
        context = {
            'cardata': cardata,
        } 
    return render(request,'carstatus.html',context)

def carimage(request):
    data = Car.objects.exclude(status='sold')
    context = {
        'data':data,
        'id':id,
    }
    return render(request,'carimage.html',context)    

def apicall(request):
    data = Apicall.objects.all()     
    response = requests.get('https://api.covid19api.com/countries').json()
    data = response
    print(data,"-=-=-=")
    print(type(data),"-=-=-=-=")
   
   
    return render(request,'apicall.html',{'data':data})  
    


 

   
    
            
                                              

                    






    
     
    
        



