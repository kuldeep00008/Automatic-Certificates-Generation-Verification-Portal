from django.urls import path
from . import views
urlpatterns =[
    path('',views.index,name='index'),
    path('Home', views.home, name='home'),
    path('logUser',views.logUser,name ='logUser'),
    path('registration',views.registration,name ='registration'),
    path('logoutView',views.logoutView,name ='logoutView'),
    path('generate',views.generate,name ='generate'),
    path('verify/<str:slug>',views.verify,name ='verify'),
    

]