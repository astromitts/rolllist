from django.db import models
from datetime import datetime


class Day(models.Model):
    date = models.DateField(default=datetime.today())


class ScheduleItem(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    start_time = models.TimeField()
    end_time = models.TimeField()


class ToDoItem(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
