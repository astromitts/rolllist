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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rolllist import views


urlpatterns = [
    path('', views.day_view),
    path('admin/', admin.site.urls),
    path('getschedule/<str:datestr>/', views.schedule_view, name='get_schedule'),
    path('gettodolist/<str:datestr>/', views.todo_list_view, name='get_todo'),
    path('additem/<str:datestr>/<int:start_time_int>/', views.add_item_form, name='add_item'),
    path('deleteitem/<int:item_id>/', views.delete_item, name='delete_item'),
    path('addtodoitem/<int:list_id>/', views.add_to_do_item_form, name='add_todo_item'),
    path('rollovertodo/<str:datestr>/', views.rollover_todo, name='rollover_todo'),
    path('deletetodoitem/<int:item_id>/', views.delete_todo_item, name='delete_todo_item'),
    path('completetodoitem/<int:item_id>/', views.complete_todo_item, name='complete_todo_item'),
    path('reverttodoitem/<int:item_id>/', views.revert_todo_item, name='revert_todo_item'),
    path('<str:datestr>/', views.day_view, name='day_view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
