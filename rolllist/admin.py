from django.contrib import admin
from .models.appmodels import (
    Day,
    ScheduleItem,
    RecurringScheduleItem,
    ToDoItem
)

# Register your models here.
admin.site.register(Day)
admin.site.register(ScheduleItem)
admin.site.register(RecurringScheduleItem)
admin.site.register(ToDoItem)
