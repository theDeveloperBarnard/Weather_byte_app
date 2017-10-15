# -*- coding: utf-8 -*-
from __future__       import unicode_literals
from django.http      import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from .models          import MyUsers,Weather,Weather_Component
from django.template  import loader
from django.http      import Http404
from django.urls      import reverse
from django.views     import generic
from django.utils     import timezone
from .forms           import RegistrationForm,LoginForm
from passlib.hash     import pbkdf2_sha256
from django           import forms
from datetime import date,datetime
import json
import requests
import datetime

my_city_list = []

def ten_day(request,user_id):
    try:
        user = MyUsers.objects.get(pk=user_id)
    except MyUsers.DoesNotExist:
        return HttpResponseRedirect(reverse('weather_byte_app:register',args=(1,)))
    else:
        ten_day_weather  = Weather.objects.get(app_code="1",user_id=user,weather_date=date.today(),weather_area=user.user_location,weather_type_code="10dw")
        weather_list_one = Weather_Component.objects.filter(weather_id=ten_day_weather)[0:5]
        weather_list_two = Weather_Component.objects.filter(weather_id=ten_day_weather)[5:10]
        return render (request, 'weather_byte_app/ten_day.html',{'weather_list_one':weather_list_one,'weather_list_two':weather_list_two,'user':user})

def detailed(request):
    return render (request, 'weather_byte_app/homepage.html')

def homepage(request, user_id,page=0):
    user_location=""
    today_date = date.today()
    try:
        user = MyUsers.objects.get(pk=user_id)
    except MyUsers.DoesNotExist:
        return HttpResponseRedirect(reverse('weather_byte_app:register',args=(1,)))
    else:
        if user.user_location == "Auto":
           response        = request.get("http://api.wunderground.com/api/3140b82d0c92e7ea/geolookup/q/autopip.json")
           location        = response.json()
           user_location = weather.get('response').get('results').get('city')
        else:
            user_location = user.user_location
        try:
            check_data      = Weather.objects.get(weather_date=today_date,user_id=user)
        except (Weather.DoesNotExist):
            new_weather_three_day = Weather(app_code="1",user_id = user,weather_type_code="03dw",weather_area=user_location,weather_date=today_date)
            new_weather_ten_day   = Weather(app_code="1",user_id = user,weather_type_code="10dw",weather_area=user_location,weather_date=today_date)
            new_weather_three_day.save()
            new_weather_ten_day.save()
            response        = requests.get("http://api.wunderground.com/api/3140b82d0c92e7ea/forecast/q/South_Africa/" + user_location + ".json")
            weather         = response.json()
            weather_list    = weather.get('forecast').get('simpleforecast').get('forecastday')
            for period in weather_list:
                minimum      = period.get('low').get('celsius')
                maximum      = period.get('high').get('celsius')
                icon         = period.get('icon_url')
                rain         = period.get('qpf_allday').get('mm')
                description  = period.get('conditions')
                today_datetime = datetime.datetime.today()
                weather_comp = Weather_Component(weather_id = new_weather_three_day,weather_comp_datetime=today_datetime,
                                                 weather_comp_icon_url = icon,weather_comp_min_temp = minimum,weather_comp_max_temp = maximum,
                                                 weather_comp_rain = rain,weather_comp_description = description)
                weather_comp.save()
                
            response_ten      = requests.get("http://api.wunderground.com/api/3140b82d0c92e7ea/forecast10day/q/South_Africa/" + user_location + ".json")
            weather_ten      = response_ten.json()
            weather_list_ten = weather_ten.get("forecast").get("simpleforecast").get("forecastday")
            for period in weather_list_ten:
                minimum = period.get('low').get('celsius')
                maximum = period.get('high').get('celsius')
                icon    = period.get('icon_url')
                rain    = period.get('qpf_allday').get('mm')
                weather_day_name = period.get('date').get('weekday')
                weather_day      = period.get('date').get('day')
                weather_month    = period.get('date').get('monthname_short')
                weather_year     = period.get('date').get('year')
                weather_date     = "{} {} {} {}".format(weather_day_name,weather_day,weather_month,weather_year)
                description      = "NA"
                weather_comp  = Weather_Component(weather_id = new_weather_ten_day,weather_comp_datetime=weather_date,
                                                 weather_comp_icon_url = icon,weather_comp_min_temp = minimum,weather_comp_max_temp = maximum,
                                                 weather_comp_rain = rain,weather_comp_description = description)
                weather_comp.save()
        except(Weather.MultipleObjectsReturned):
            a = ""
        today_weather = Weather.objects.get(app_code="1",user_id=user,weather_date=date.today(),weather_area=user.user_location,weather_type_code="03dw")
        weather_list  = Weather_Component.objects.filter(weather_id=today_weather)[0]
        user = MyUsers.objects.get(pk=user_id)
        return render (request, 'weather_byte_app/homepage.html',{'weather_list':weather_list,'user':user})

def landingPage(request):
    form = LoginForm()
    return render(request, 'weather_byte_app/login.html',{'form':form})

def register(request,error=0):
    form      = RegistrationForm()
    if error != 0:
        return render(request, 'weather_byte_app/registration.html', {'form':form,'error_message':"Something has gone wrong.",})
    else:
        return render(request, 'weather_byte_app/registration.html',{'form':form})

def login(request):
    try:
        if request.POST["register"] != "":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                new_user=form.save(commit=False)
                try:
                    selected_user = MyUsers.objects.get(user_username = new_user.user_username)
                except MyUsers.DoesNotExist:
                    hash = pbkdf2_sha256.encrypt(new_user.user_password, rounds=200000, salt_size=16)
                    new_user = MyUsers(user_username = new_user.user_username,user_email=new_user.user_email,user_password=hash,
                                       user_first_name=new_user.user_first_name,user_last_name=new_user.user_last_name,
                                       user_location=new_user.user_location,user_apps='1',pub_date=timezone.now())
                    new_user.save()
                    return HttpResponseRedirect(reverse('weather_byte_app:homepage',args=(new_user.pk,)))
                else:
                    return render(request, 'weather_byte_app/registration.html', {'form':form,'error_message':"A user with the user Name " + str(name) + " already exists",})
            else:
                return render(request,'weather_byte_app/registration.html', {'form':form,'error_message':"Something went wrong",})
    except KeyError:
            form     = LoginForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                try:
                    current_user = MyUsers.objects.get(user_username = user.user_username)
                except IndexError:
                    return render(request, 'weather_byte_app/login.html', {'error_message':"Invalid login details"})
                else:
                    hash = current_user.user_password
                    if pbkdf2_sha256.verify(user.user_password, hash) == True:
                        return HttpResponseRedirect(reverse('weather_byte_app:homepage',args=(current_user.pk,)))
                    else:
                        return render(request, 'weather_byte_app/login.html', {'form':form,'error_message':"Invalid password"})
            else:
               return render(request, 'weather_byte_app/login.html', {'error_message':"Something has gone wrong"})

