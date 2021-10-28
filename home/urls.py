from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('covid_hospitals', views.covid_hospitals, name='covid_hospitals'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    #path('register', views.register, name='register'),
    #path('login', views.login, name='login'),
]