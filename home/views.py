from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Feedback
import requests
import json
# from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib import messages
from django import forms
from django.contrib.auth import login
from users.models import CustomUser, Profile
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests 
from bs4 import BeautifulSoup 


# Create your views here.
def index(request):
    url1 = "https://covid-193.p.rapidapi.com/statistics"
    url2 = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

    querystring = {"country":"India"}

    headers1 = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "8fb8aad444mshea7418dbc654619p1d71bfjsn8ba39400da5d"
        }

    headers2 = {
    'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
    'x-rapidapi-key': "8fb8aad444mshea7418dbc654619p1d71bfjsn8ba39400da5d"
    }

    response = requests.request("GET", url1, headers=headers1, params=querystring).json()
    result = requests.request("GET", url2, headers=headers2).json()

    data = response['response']
    state = result['state_wise']
    d = data[0]
    print(d)
    context = {
        'all': d['cases']['total'],
        'recovered': d['cases']['recovered'],
        'deaths': d['deaths']['total'],
        'new': d['cases']['new'],
        'critical': d['cases']['critical'],
        'tests': d['tests']['total'],
        'state': state
    }
    return render(request, 'index.html', context)
    # return HttpResponse('This is Home Page')

def covid_hospitals(request):
    hospital = CustomUser.objects.all()
    healthcare_services = Profile.objects.all()
    mylist = zip(hospital, healthcare_services)
    context = {
            'mylist': mylist,
        }
    return render(request, 'covid_hospitals.html', context)

def contact(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        remark = request.POST.get('remark')
        feedback = Feedback(firstname=firstname, lastname=lastname, email=email, phone=phone, remark=remark, date=datetime.today())
        feedback.save()
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')



