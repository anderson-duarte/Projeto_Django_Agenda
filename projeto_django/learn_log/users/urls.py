
from django.conf.urls import url
from django.contrib.auth import login
from . import views

urlpatterns = [
    url(r'^login/$', login, 'users/login.html', name='login'),
]