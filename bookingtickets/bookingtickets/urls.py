"""
URL configuration for bookingtickets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from Ridehub.views import Ride,bus_info,Users_details,bus_list,busbooking,make_payment,update_ticket,delete_ticket

urlpatterns = [
     path('admin/', admin.site.urls), 
    path('RideHub/',Ride),
    path('bus/',bus_info),
    path('user/',Users_details),
    path('buses/',bus_list),
    path('bookings/',busbooking),
    path('make_payment/',make_payment),
    path('update/<int:id>/', update_ticket),
    # path('update/',update_ticket),
    path('delete/',delete_ticket),

]
