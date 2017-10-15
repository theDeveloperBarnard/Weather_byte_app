# -*- coding: utf-8 -*-
from __future__   import unicode_literals
from django.db    import models
from django.utils import timezone
import json
import requests

my_dict   = {}
response  = requests.get("http://api.wunderground.com/api/3140b82d0c92e7ea/geolookup/q/South_Africa.json")
weather   = response.json()
my_dict["city"] = weather.get('response').get('results')
my_list = my_dict.get('city')
my_city_list = []

for city in my_list:
    my_city_list.append(city.get('city'))

my_city_list.append('Cape Town')
my_city_list.sort()
my_city_list.insert(0,'Auto')

CITIES = [(x,x) for x in my_city_list]

class MyUsers(models.Model):
    user_username   = models.CharField(max_length=20)
    user_email      = models.CharField(max_length=20)
    user_password   = models.CharField(max_length=200)
    user_first_name = models.CharField(max_length=20)
    user_last_name  = models.CharField(max_length=100)
    user_location   = models.CharField(max_length=200,choices=CITIES)
    user_apps       = models.CharField(max_length=100)
    pub_date        = models.DateTimeField('Registered Date')

    def __str__(self):
        return self.user_username
    
    

class Weather(models.Model):
    app_code = models.CharField(max_length=100,default = "1")
    user_id  = models.ForeignKey(MyUsers, on_delete=models.CASCADE, default=1)
    weather_type_code = models.CharField(max_length=3,default="trdw")
    weather_area      = models.CharField(max_length=100)
    weather_date      = models.DateField('Published Date')

    class Meta:
        indexes = [
            models.Index(fields=['app_code','user_id','weather_date','weather_area','weather_type_code'], name = 'idxw1'),
        ]

    def __str__(self):
        return str(self.weather_type_code) + " " + str(self.weather_date)
    
class Weather_Component(models.Model):
    weather_id               = models.ForeignKey(Weather,on_delete=models.CASCADE,default=1)
    weather_comp_datetime    = models.CharField(max_length=200)
    weather_comp_icon_url    = models.CharField(max_length=200)
    weather_comp_min_temp    = models.CharField(max_length=10)
    weather_comp_max_temp    = models.CharField(max_length=10)
    weather_comp_rain        = models.CharField(max_length=100)
    weather_comp_description = models.CharField(max_length=200)
    weather_comp_label       = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['weather_id','weather_comp_datetime'],name='idxwc1'),
            ]
    
