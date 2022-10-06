from distutils.command.upload import upload
from pyexpat import model
from tkinter import CASCADE
from typing_extensions import Self
from unittest.util import _MAX_LENGTH
from wsgiref.validate import validator
import os
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator,MinMoneyValidator
from moneyed import USD
from djmoney.money import Money
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django_google_maps import fields as map_fields

condition_choices = (
    ('poor','poor'),
    ('fair','fair'),
    ('good','good'),
    ('excellent','excellent')
)
car_status = (
    ('available','available'),
    ('sold','sold'),
)

def get_image_path(instance,filename):
    return os.path.join('car',str(instance.Car.id),filename)

class Car(models.Model):
    seller_name = models.CharField(max_length=100)
    seller_mobile = models.CharField(max_length=10)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image = models.FileField(null=True,upload_to="car/")
    year = models.DateField()
    condition = models.CharField(max_length=20, choices=condition_choices)
    asking_price = MoneyField(max_digits=10,decimal_places=2,default_currency='USD',
    validators=[MinMoneyValidator(Money(1000,'USD')),MaxMoneyValidator(Money(100000,'USD'))])
    status = models.CharField(max_length=20,choices = car_status,null=True)
    User = models.ForeignKey('User',on_delete=models.CASCADE,null=True)

    def __str__(self):    
        return self.seller_name,

class  BuyCar(models.Model):
    Car = models.ForeignKey(Car,on_delete=models.CASCADE,null=True)   
    buyer_name = models.CharField(max_length=50)
    buyer_number = models.CharField(max_length=10)
    commission = MoneyField(max_digits=10,decimal_places=2,default_currency='USD',default=0)
    net_amount = MoneyField(max_digits=10,decimal_places=2,default_currency='USD',default=0) 
    User = models.ForeignKey('User',on_delete=models.CASCADE,null=True)
        
    def _str_(self):
        return self.buyer_name

    @property
    def commission(self):
        commission = (self.Car.asking_price * 5) /100  
        return commission  

    @property
    def net_amount(self):
        commission = (self.Car.asking_price * 5) /100       
        net_amount = (self.Car.asking_price) - commission 
        return net_amount    

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),max_length=50,unique=True)
    phone_no = models.CharField(max_length=10)
    address = map_fields.AddressField(max_length=200,null=True)
    geolocation = map_fields.GeoLocationField(max_length=100,null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  []
    objects = UserManager()

class CarImage(models.Model):
    Car = models.ForeignKey(Car,on_delete=models.CASCADE,null=True) 
    image = models.FileField(upload_to=get_image_path)



    










