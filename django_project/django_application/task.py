from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from django_project import settings
from .forms import CarForm,UserForm,BuyForm
from .models import Car,BuyCar
from django.shortcuts import redirect, render

@shared_task(bind=True)
def send_mail_func(request,id):
    cardata = Car.objects.get(id=id)
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
    
