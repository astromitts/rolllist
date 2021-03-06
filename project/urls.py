from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from rolllist import views
from rolllistuser import views as userviews


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # user handlers
    path('user/', userviews.user_profile, name='user_profile'),
    path('user/changepassword/', userviews.change_password, name='user_change_password'),
    path('about/', TemplateView.as_view(template_name='rolllist/about.html'), name='about'),
    path('login/', userviews.login_handler, name='login_handler'),
    path('logout/', userviews.logout_handler, name='logout_handler'),
    path('user/create/', userviews.create_handler, name='create_user_handler'),


    # dashboard ajax views
    path('getschedule/<str:datestr>/', views.schedule_view, name='get_schedule'),
    path('gettodolist/<str:datestr>/', views.todo_list_view, name='get_todo'),

    # schedule item handlers
    path('editscheduleitem/<int:item_id>/', views.edit_schedule_item_form, name='edit_item'),
    path('addscheduleitem/<str:datestr>/<int:start_time_int>/', views.add_schedule_item_form, name='add_item'),
    path('deletescheduleitem/<int:item_id>/', views.delete_schedule_item_handler, name='delete_item_handler'),
    path('recurringschedule/', views.manage_recurring_items, name='manage_recurring_items'),
    path('recurringschedule/<int:item_id>/edit/', views.edit_recurring_item_handler, name='edit_recurring_item'),
    path('recurringschedule/<int:item_id>/delete/', views.delete_recurring_item_handler, name='delete_recurring_item'),

    # to do list item handlers
    path('addtodoitem/<str:datestr>/', views.add_to_do_item_form, name='add_todo_item'),
    path('rollovertodo/<str:datestr>/', views.rollover_todo, name='rollover_todo'),
    path('edittodoitem/<int:item_id>/', views.edit_to_do_item_form, name='edit_todo_item'),
    path('deletetodoitem/<int:item_id>/', views.delete_todo_item, name='delete_todo_item'),
    path('completetodoitem/<int:item_id>/', views.complete_todo_item, name='complete_todo_item'),
    path('reverttodoitem/<int:item_id>/', views.revert_todo_item, name='revert_todo_item'),
    path('movekanabanitem/<int:item_id>/<str:target_status>/', views.move_kanban_item, name='move_kanban_item'),

    # dashboard
    path('<str:datestr>/', views.day_view, name='day_view'),
    path('', views.day_view, name='dashboard'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
