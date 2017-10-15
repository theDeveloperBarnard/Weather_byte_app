from django.conf.urls import include,url

from . import views

app_name = "weather_byte_app"
urlpatterns = [
    url(r'^$',views.landingPage,name='landingPage'),
    url(r'^register/$',views.register,name='register'),
    url(r'^(?P<error>[0-9]+)/register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^(?P<user_id>[0-9]+)/homepage/$',views.homepage,name='homepage'),
    url(r'^(?P<user_id>[0-9]+)/ten_day/$', views.ten_day,name='ten_day'),
]
