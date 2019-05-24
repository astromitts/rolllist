from django.db import models
from datetime import datetime

from rolllist.utils import time_options_strings


class BaseModel(object):
    """ Base abstract model for common functions
    """
    @classmethod
    def get_or_create(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs), False
        except cls.DoesNotExist:
            newcls = cls()
            for key, val in kwargs.items():
                setattr(newcls, key, val)
            newcls.save()
            return newcls, True


# TODO add a user class and hook to Day
class Day(models.Model, BaseModel):
    """ Model to link items to a specific day """
    date = models.DateField(default=datetime.today, unique=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return '{0:%B %d %Y}'.format(self.date)


class ScheduleItem(models.Model, BaseModel):
    """ Model for schedule items
    """
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
        """ Front end helper to display human version of start time interval """
        return time_options_strings[self.start_time]

    @property
    def end(self):
        """ Front end helper to display human version of end time interval """
        return time_options_strings[self.end_time]

    # TODO probably need a new model for recurring items
    @classmethod
    def rollover_recurring_items(cls, day):
        for item in cls.objects.filter(recurring=True).all():
            item.day = day
            item.save()


class ToDoList(models.Model, BaseModel):
    """ Model for linking together to do items to a day
    """
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    rolled_over = models.BooleanField(default=False)  # TODO: implement

    def __str__(self):
        return 'list for day %s' % self.day


class ToDoItem(models.Model, BaseModel):
    """ Model for to do items """
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s)' % (self.title, self.to_do_list)
