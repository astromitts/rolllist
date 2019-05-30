from django.db import models
from datetime import datetime, timedelta
from itertools import chain
from operator import attrgetter

from rolllistuser.models import RollListUser
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


class Day(models.Model, BaseModel):
    """ Model to link items to a specific day """
    date = models.DateField(default=datetime.today, unique=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return '{0:%B %d %Y}'.format(self.date)

    def get_schedule_items(self, user):
        """ Function to return a full list of scheduled items for a day
            including regular items and recurring items
        """
        recurring_item_set = user.recurringscheduleitem_set.all()
        item_set = self.scheduleitem_set.all()
        full_list = sorted(
            chain(recurring_item_set, item_set),
            key=attrgetter('start_time')
        )
        return full_list


class ScheduleItemMixin(object):

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


class RecurringScheduleItem(models.Model, ScheduleItemMixin, BaseModel):
    user = models.ForeignKey(RollListUser, on_delete=models.CASCADE)
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

    def __str__(self):
        return '%s // %s (@%s-%s)' % (self.title, self.location, self.start, self.end)

    @property
    def get_delete_url(self):
        return '/deletescheduleitemform/%d/1/' % self.id


class ScheduleItem(models.Model, ScheduleItemMixin, BaseModel):
    """ Model for schedule items
    """
    user = models.ForeignKey(RollListUser, on_delete=models.CASCADE)
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

    def __str__(self):
        return '%s // %s (%s@%s-%s)' % (
            self.title, self.location, self.day, self.start, self.end
        )

    @property
    def get_delete_url(self):
        return '/deletescheduleitemform/%d/0/' % self.id

    def make_recurring(self):
        if not self.recurrance:
            new_recurrance = RecurringScheduleItem(
                title=self.title,
                location=self.location,
                start_time=self.start_time,
                end_time=self.end_time,
                user=self.user
            )
            new_recurrance.save()
            self.recurrance = new_recurrance
            self.save()


class ToDoList(models.Model, BaseModel):
    """ Model for linking together to do items to a day
    """
    user = models.ForeignKey(RollListUser, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    rolled_over = models.BooleanField(default=False)  # TODO: implement

    class Meta:
        unique_together = ('user', 'day',)

    def __str__(self):
        return 'list for day %s' % self.day

    def rollover_items(self):
        previous_day_date = self.day.date - timedelta(days=1)
        source_day = Day.objects.get(date=previous_day_date)
        source_list, created = ToDoList.get_or_create(
            day=source_day,
            user=self.user
        )
        for item in source_list.todoitem_set.filter(completed=False).all():
            new_item = ToDoItem(title=item.title, to_do_list=self)
            new_item.save()


class ToDoItem(models.Model, BaseModel):
    """ Model for to do items """
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s)' % (self.title, self.to_do_list)
