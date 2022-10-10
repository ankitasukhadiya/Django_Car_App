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
def send_email_task(id):
    data = BuyCar.objects.filter(id=id)
    print(data.id,"=-=--=-=--=-=")
    mail_subject = "Hi! Celery Testing"
    message = "If you are liking my content, please hit the like button and do subscribe to my channel"
    to_email = data.email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "Done"
    # print(id,"-=-=-=-==-=-=-=-=-=--=-=",data)
    # subject = f'BuyCar {data.buyer_name}'
    # template =  render_to_string('mail.html',{'buyer_name':data.buyer_name,'buyer_number':data.buyer_number,
    #         'seller_name':data.Car.seller_name,'seller_mobile':data.Car.seller_mobile,'make':data.Car.make,
    #         'model':data.Car.model,'year':data.Car.year,'condition':data.Car.condition,
    #         'asking_price':data.Car.asking_price,'commission':data.commission,'net_amount':data.net_amount}) , 
    # msg = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER])   
    # msg.content_subtype = 'html'
    # # msg.delay()
    # msg.send()
        # send_mail(subject,template,msg)

    


    
