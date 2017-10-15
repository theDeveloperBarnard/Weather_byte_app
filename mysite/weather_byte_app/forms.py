from django import forms
from weather_byte_app.models import MyUsers
from django.forms import ModelForm
import json
import requests

class RegistrationForm(ModelForm):

    class Meta:
        model = MyUsers
        fields = ['user_username','user_email','user_password',
                  'user_first_name','user_last_name','user_location']
        widgets = {
        'user_password': forms.PasswordInput(),
        }
        labels = {
        'user_username': 'Username'
        }
        
class LoginForm(ModelForm):
    class Meta:
        model = MyUsers
        fields = ['user_username','user_password']
        widgets = {
        'user_password': forms.PasswordInput(),
        }
