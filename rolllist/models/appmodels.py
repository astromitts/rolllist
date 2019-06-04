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

    @property
    def to_url_str(self):
        return "{0:%Y%m%d}".format(self.date)

    @property
    def to_str(self):
        return self.__str__

    @classmethod
    def get_from_str(cls, datestr):
        target_date = datetime.strptime(datestr, "%Y%m%d").date()
        target_day, created = cls.get_or_create(date=target_date)
        return target_day, created

    @property
    def display_string(self):
        return '{0:%Y%m%d}'.format(self.date)


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
        for source_item in source_list.todoitem_set.filter(completed=False, rolled_over=False).all():
            new_item = ToDoItem(
                title=source_item.title,
                to_do_list=self,
                days_incomplete=source_item.days_incomplete + 1
            )
            new_item.save()
            source_item.rolled_over = True
            source_item.save()

    def get_items(self):
        return self.todoitem_set.order_by('-days_incomplete', '-priority', 'id').all()


class ToDoItem(models.Model, BaseModel):
    """ Model for to do items """
    priority_choices = [
        (1, 'low'),
        (2, 'medium'),
        (3, 'high'),
    ]
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)
    rolled_over = models.BooleanField(default=False)  # TODO: implement
    days_incomplete = models.IntegerField(default=1)
    priority = models.IntegerField(default=1, choices=priority_choices)

    def __str__(self):
        return '%s (%s)' % (self.title, self.to_do_list)

    class Meta:
        ordering = ['-priority', '-days_incomplete', 'id']


class Note(models.Model, BaseModel):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    user = models.ForeignKey(RollListUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_all_for_user_by_day(cls, user):
        all_notes = cls.objects.filter(user=user).order_by('day', 'updated_at').all()
        notes_by_date = {}
        for note in all_notes:
            if note.day not in notes_by_date.keys():
                notes_by_date[note.day] = []
            notes_by_date[note.day].append(note)
        return notes_by_date
