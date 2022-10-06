from django import forms
from django.forms import ModelForm
from .models import Car, User,BuyCar
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type =  'date'

class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ["seller_name","seller_mobile","make","model","image","year","condition","asking_price"]  
        widgets = {
            'year' : DateInput(),
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        } 
class UserForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "phone_no")       

class BuyForm(ModelForm):
    class Meta:
        model = BuyCar   
        fields = ("buyer_name","buyer_number")                                                                                                                                                                                                                                                                                                                                           