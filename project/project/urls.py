"""project URL Configuration

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
from django.urls import path
from timelord import views as tl

urlpatterns = [
    path('admin/', admin.site.urls),
    path('today/', tl.day_view),
    path('additem/<str:datestr>/<int:start_time_int>/', tl.add_item_form, name='add_item'),
    path('addtodoitem/<str:datestr>/', tl.add_to_do_item_form, name='add_todo_item'),
    path('<str:datestr>/', tl.day_view, name='day_view'),
]
