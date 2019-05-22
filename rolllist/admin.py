from django.contrib import admin
from .models.appmodels import Day, ScheduleItem, ToDoItem

# Register your models here.
admin.site.register(Day)
admin.site.register(ScheduleItem)
admin.site.register(ToDoItem)
