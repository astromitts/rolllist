from django.contrib import admin
from rolllist.models.appmodels import (
    Day,
    ScheduleItem,
    RecurringScheduleItem,
    ToDoList,
    ToDoItem,
    Note,
)

# Register your models here.
admin.site.register(Day)
admin.site.register(Note)
admin.site.register(ScheduleItem)
admin.site.register(RecurringScheduleItem)
admin.site.register(ToDoItem)
admin.site.register(ToDoList)
