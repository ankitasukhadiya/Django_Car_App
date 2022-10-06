from multiprocessing import context
import pdb
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib import messages
from .models import Car,BuyCar,User,CarImage
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
    cardata = Car.objects.get(id=id)
  
    # if cardata.status != 'sold':
    if request.method == 'POST':
            form = BuyForm(request.POST,request.FILES)
            if form.is_valid():
                buyername = form.cleaned_data.get('buyer_name')
                print(buyername,"----")
                buyernumber = form.cleaned_data.get('buyer_number')
                print(buyernumber,"////")   
                buycarobj = BuyCar(Car=cardata,buyer_name= buyername,buyer_number=buyernumber)
                buycarobj.save()    
                return redirect("django_application:success")
            else:    
                return render(request,"buycar.html",{'form':form,'cardata':cardata})   
    cardata.status = 'sold'
    cardata.save()
    form = BuyForm(request.POST)
    return render(request,"buycar.html",{'form':form,'cardata':cardata}) 

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


 

   
    
            
                                              

                    






    
     
    
        



