from django.contrib import admin
from django.conf import settings
from .models import Car,User,BuyCar,CarImage


admin.site.register(CarImage)
admin.site.register(Car)
admin.site.register(User)
admin.site.register(BuyCar)

