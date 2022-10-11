from multiprocessing import context
from django.http import HttpResponse
from django_project.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from .forms import CarForm,UserForm,BuyForm
from .models import Car,BuyCar
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from time import sleep

@shared_task(bind=True)
def send_email_task(request, id, email):
    data = BuyCar.objects.get(id=id) 
    subject = f'BuyCar {data.buyer_name}'
    message='Buy Car Detail ... '
    context = {'buyer_name':data.buyer_name,'buyer_number':data.buyer_number,
            'seller_name':data.Car.seller_name,'seller_mobile':data.Car.seller_mobile,'make':data.Car.make,
            'model':data.Car.model,'year':data.Car.year,'condition':data.Car.condition,
            'asking_price':data.Car.asking_price,'commission':data.commission,'net_amount':data.net_amount}
    template =  render_to_string('mail.html',context) 
    from_mail = EMAIL_HOST_USER
    to_email = email 
    # sleep(120)
    send_mail(
        subject=subject,
        message=message,
        html_message=template,
        from_email=from_mail,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "done"

    


    
