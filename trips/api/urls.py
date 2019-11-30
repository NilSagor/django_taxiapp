"""taxi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 

from trips.api.views import SignUpView, LogInView, LogOutView, TripView

app_name = 'taxi'
urlpatterns = [    
    # path('sign_up/', SignUpView.as_view(), name = 'sign_up'),
    # path('log_in/', LogInView.as_view(), name = 'log_in'),
    # path('log_out/', LogOutView.as_view(), name = 'log_out'),
    path('', TripView.as_view({'get': 'list'}), name = 'trip_list'),
]
