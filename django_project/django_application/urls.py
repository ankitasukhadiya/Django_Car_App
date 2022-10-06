from django import views
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
app_name = 'django_application'

urlpatterns = [
    path('home/',views.home, name='home'),
    path('base/',views.base, name='base'),
    path('carlist/',views.carlist, name='carlist'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('findcar/',views.findcar, name='findcar'),
    path('signup/',views.signup, name = 'signup'),
    path('login/',views.login, name = 'login'),
    path('logout/',views.logout, name = 'logout'),
    path('buycardetail/<int:id>',views.buycardetail, name = 'buycardetail'),
    path('cardetail/<int:id>',views.cardetail, name = 'cardetail'),
    path('buycar/<int:id>',views.buycar, name = 'buycar'),
    path('success/',views.success, name = 'success'),
    path('carstatus/',views.carstatus, name = 'carstatus'),
    path('carimage/',views.carimage, name = 'carimage'),

]