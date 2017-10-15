# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import MyUsers,Weather,Weather_Component

admin.site.register(MyUsers)
admin.site.register(Weather)
admin.site.register(Weather_Component)

# Register your models here.
