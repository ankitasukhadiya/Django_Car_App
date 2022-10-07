from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from django_project import settings
from .forms import CarForm,UserForm,BuyForm
from .models import Car,BuyCar
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from time import sleep

@shared_task(bind=True)
# def send_mail(sender,instance,created,**kwargs):
    
#     if created:
#         subject = f'BuyCar {instance.buyer_name}'
#         template = render_to_string('mail.html',{'buyer_name':instance.buyer_name,'buyer_number':instance.buyer_number,
#         'seller_name':instance.Car.seller_name,'seller_mobile':instance.Car.seller_mobile,'make':instance.Car.make,
#         'model':instance.Car.model,'year':instance.Car.year,'condition':instance.Car.condition,
#         'asking_price':instance.Car.asking_price,'commission':instance.commission,'net_amount':instance.net_amount})       
#         msg = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER])   
#         msg.content_subtype = 'html'
#         msg.delay()
#         msg.send()

def send_email_task(sender,instance,created):
    sender = BuyCar
    sleep(20)
    send_mail(
        subject = f'BuyCar {instance.buyer_name}',
        template = render_to_string('mail.html',{'buyer_name':instance.buyer_name,'buyer_number':instance.buyer_number,
        'seller_name':instance.Car.seller_name,'seller_mobile':instance.Car.seller_mobile,'make':instance.Car.make,
        'model':instance.Car.model,'year':instance.Car.year,'condition':instance.Car.condition,
        'asking_price':instance.Car.asking_price,'commission':instance.commission,'net_amount':instance.net_amount}) ,  
        
        fail_silently=False,
    )


    
