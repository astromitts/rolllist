from django.db import models
from datetime import datetime

from rolllist.utils import time_options_strings


# TODO add a user class and hook to Day
class Day(models.Model):
    date = models.DateField(default=datetime.today, unique=True)

    class Meta:
        ordering = ['date']

    @property
    def url_str(self):
        return '{0:%Y%m%d}'.format(self.date)

    def __str__(self):
        return '{0:%B %d %Y}'.format(self.date)

    @classmethod
    def get_or_create(self, date):
        try:
            return self.objects.get(date=date), False
        except self.DoesNotExist:
            newday = self(date=date)
            newday.save()
            return newday, True


class ScheduleItem(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    start_time = models.IntegerField(
        choices=[
            (i, time_options_strings[i]) for i in range(0, len(time_options_strings))
        ]
    )
    end_time = models.IntegerField(
        choices=[
            (i, time_options_strings[i]) for i in range(0, len(time_options_strings))
        ]
    )
    location = models.CharField(max_length=150, null=True)

    recurring = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return '%s // %s (%s)' % (self.title, self.location, self.day)

    @property
    def start(self):
        return time_options_strings[self.start_time]

    @property
    def end(self):
        return time_options_strings[self.end_time]

    @classmethod
    def rollover_recurring_items(self, day):
        for item in self.objects.filter(recurring=True).all():
            item.day = day
            item.save()


class ToDoList(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    rolled_over = models.BooleanField(default=False)

    @classmethod
    def get_or_create(self, day):
        try:
            return self.objects.get(day=day)
        except self.DoesNotExist:
            newlist = self(day=day)
            newlist.save()
            return newlist

    def __str__(self):
        return 'list for day %s' % self.day


class ToDoItem(models.Model):
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s)' % (self.title, self.to_do_list)
