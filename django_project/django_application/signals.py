from email import message
from urllib import request
from django.core .mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import BuyCar
# from django.contrib.auth.models import BuyCar

@receiver(post_save,sender=BuyCar)
def send_mail(sender,instance,created,**kwargs):
    if created:
        subject = f'BuyCar {instance.buyer_name}'
        template = render_to_string('mail.html',{'buyer_name':instance.buyer_name,'buyer_number':instance.buyer_number,
        'seller_name':instance.Car.seller_name,'seller_mobile':instance.Car.seller_mobile,'make':instance.Car.make,
        'model':instance.Car.model,'year':instance.Car.year,'condition':instance.Car.condition,
        'asking_price':instance.Car.asking_price,'commission':instance.commission,'net_amount':instance.net_amount})       
        msg = EmailMultiAlternatives(subject,template,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER])   
        msg.content_subtype = 'html'
        msg.send()
    