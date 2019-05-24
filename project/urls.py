from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rolllist import views


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # dashboard
    path('', views.day_view),
    path('<str:datestr>/', views.day_view, name='day_view'),

    # dashboard ajax views
    path('getschedule/<str:datestr>/', views.schedule_view, name='get_schedule'),
    path('gettodolist/<str:datestr>/', views.todo_list_view, name='get_todo'),

    # schedule item handlers
    path('addscheduleitem/<str:datestr>/<int:start_time_int>/', views.add_schedule_item_form, name='add_item'),
    path('deletescheduleitem/<int:item_id>/', views.delete_schedule_item, name='delete_item'),

    # to do list item handlers
    path('addtodoitem/<int:list_id>/', views.add_to_do_item_form, name='add_todo_item'),
    path('rollovertodo/<str:datestr>/', views.rollover_todo, name='rollover_todo'),
    path('deletetodoitem/<int:item_id>/', views.delete_todo_item, name='delete_todo_item'),
    path('completetodoitem/<int:item_id>/', views.complete_todo_item, name='complete_todo_item'),
    path('reverttodoitem/<int:item_id>/', views.revert_todo_item, name='revert_todo_item'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
