from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rolllist import views
from rolllistuser import views as userviews


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # user handlers
    path('user/', userviews.create_init_view, name='user_init'),
    path('login/', userviews.login_handler, name='login_handler'),
    path('logout/', userviews.logout_handler, name='logout_handler'),
    path('user/create/', userviews.create_handler, name='create_user_handler'),


    # dashboard ajax views
    path('getschedule/<str:datestr>/', views.schedule_view, name='get_schedule'),
    path('gettodolist/<str:datestr>/', views.todo_list_view, name='get_todo'),

    # schedule item handlers
    path('editscheduleitem/<int:item_id>/<int:recurring>/', views.edit_schedule_item_form, name='edit_item'),
    path('addscheduleitem/<str:datestr>/<int:start_time_int>/', views.add_schedule_item_form, name='add_item'),
    path('deletescheduleitemform/<int:item_id>/<int:recurring>/', views.delete_schedule_item_handler, name='delete_item_form'),

    # schedule notes handlers
    path('viewnotes/', views.view_all_notes, name='view_all_notes'),
    path('getnotes/<str:datestr>/', views.note_view, name='get_notes'),
    path('editnote/<int:note_id>/', views.edit_note_form, name='edit_note'),
    path('addnote/<str:datestr>/', views.add_note_form, name='add_note'),
    path('editnote/<int:note_id>/<str:src>/', views.edit_note_form, name='edit_note_src'),
    path('addnote/<str:datestr>/<str:src>/', views.add_note_form, name='add_note_src'),
    path('deletenoteform/<int:note_id>/', views.delete_note_form, name='delete_note'),
    # to do list item handlers
    path('addtodoitem/<int:list_id>/', views.add_to_do_item_form, name='add_todo_item'),
    path('rollovertodo/<str:datestr>/', views.rollover_todo, name='rollover_todo'),
    path('deletetodoitem/<int:item_id>/', views.delete_todo_item, name='delete_todo_item'),
    path('completetodoitem/<int:item_id>/', views.complete_todo_item, name='complete_todo_item'),
    path('reverttodoitem/<int:item_id>/', views.revert_todo_item, name='revert_todo_item'),

    # dashboard
    path('<str:datestr>/', views.day_view, name='day_view'),
    path('', views.day_view, name='dashboard'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
