from django.db import models
from datetime import datetime, timedelta
from operator import attrgetter

from rolllistuser.models import RollListUser
from rolllist.utils import time_options_strings, weekday_strings_abbr


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
    _day_of_week = models.IntegerField()

    def save(self, *args, **kwargs):
        self._day_of_week = self.date.weekday()
        super(Day, self).save(*args, **kwargs)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return '{0:%A, %B %d %Y}'.format(self.date)

    def get_schedule_items(self, user):
        """ Function to return a full list of scheduled items for a day
            including regular items and recurring items
        """
        # check if item instances have been created for recurring items
        # if not, create them
        recurring_item_set = user.recurringscheduleitem_set.all()
        for item in recurring_item_set:
            item.set_for_day(day=self)

        # once recurrances are created, select all active items for the day
        item_set = self.scheduleitem_set.filter(is_active=True).all()
        full_list = sorted(
            item_set,
            key=attrgetter('start_time')
        )
        return full_list

    def set_recurring_items(self, user):
        recurring_item_set = user.recurringscheduleitem_set.all()
        for item in recurring_item_set:
            item.set_for_day(day=self)

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

    recurrance_0 = models.BooleanField("Monday", default=False)
    recurrance_1 = models.BooleanField("Tuesday", default=False)
    recurrance_2 = models.BooleanField("Wednesday", default=False)
    recurrance_3 = models.BooleanField("Thursday", default=False)
    recurrance_4 = models.BooleanField("Friday", default=False)
    recurrance_5 = models.BooleanField("Saturday", default=False)
    recurrance_6 = models.BooleanField("Sunday", default=False)

    def __str__(self):
        return '%s // %s (@%s-%s)' % (self.title, self.location, self.start, self.end)

    @property
    def day_of_week_display(self):
        displays = []
        for idx, display in enumerate(weekday_strings_abbr):
            day_recurrance_flag = 'recurrance_%s' % idx
            has_day = getattr(self, day_recurrance_flag)
            if has_day:
                displays.append(display)
        return ", ".join(displays)

    def set_for_day(self, day):
        # check if there should be a schedule item generated for today
        day_recurrance_flag = 'recurrance_%s' % day.date.weekday()
        item_qs = ScheduleItem.objects.filter(day=day, recurrance=self)
        item_exists = item_qs.exists()
        if getattr(self, day_recurrance_flag):
            if not item_exists:
                schedule_item = ScheduleItem(
                    user=self.user,
                    day=day,
                    title=self.title,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    location=self.location,
                    recurrance=self
                )
                schedule_item.save()
        else:
            # if the item was created by scrolling on the dashboard but the recurrance
            # for this week day is no longer true, delete the item
            if item_exists:
                item_qs.delete()

    def delete_for_day(self, day):
        # delete an instance of a recurring item's child item for a specific day
        item = ScheduleItem.objects.get(
            day=day,
            recurrance=self
        )
        item.is_active = False
        item.save()

    def delete_current_and_future(self, day):
        # first, set past instances to non-recurring to retain history
        # then delete any instances that are today or later
        scheduled_events = ScheduleItem.objects.filter(recurrance=self).all()
        for event in scheduled_events:
            if event.day.date < day.date:
                event.recurrance = None
                event.save()
            elif event.day.date >= day.date:
                event.delete()
        self.delete()

    def update_current_and_future(self, day, update_vars=None):
        # first, set past instances to non-recurring to retain history
        # then delete any instances that are today or later
        if not update_vars:
            update_vars = {}

        scheduled_events = ScheduleItem.objects.filter(recurrance=self).all()
        for event in scheduled_events:
            if event.day.date >= day.date:
                for key, val in update_vars.items():
                    setattr(event, key, val)
                    event.save()
        for key, val in update_vars.items():
            setattr(self, key, val)
            self.save()


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

    # these two fields are used to determine if an item has been rolled over from the
    # recurrance table and has not been deleted byt he user
    is_active = models.BooleanField(default=True)
    recurrance = models.ForeignKey(RecurringScheduleItem, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s // %s (%s@%s-%s)' % (
            self.title, self.location, self.day, self.start, self.end
        )

    @property
    def get_delete_url(self):
        return '/deletescheduleitemform/%d/0/' % self.id

    def make_recurring(self, requested_recurrances):
        new_recurrance = RecurringScheduleItem(
            title=self.title,
            location=self.location,
            start_time=self.start_time,
            end_time=self.end_time,
            user=self.user,
            recurrance_0=0 in requested_recurrances,
            recurrance_1=1 in requested_recurrances,
            recurrance_2=2 in requested_recurrances,
            recurrance_3=3 in requested_recurrances,
            recurrance_4=4 in requested_recurrances,
            recurrance_5=5 in requested_recurrances,
            recurrance_6=6 in requested_recurrances,
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
        all_notes = cls.objects.filter(user=user).order_by('-day', '-updated_at').all()
        notes_by_date = {}
        for note in all_notes:
            if note.day not in notes_by_date.keys():
                notes_by_date[note.day] = []
            notes_by_date[note.day].append(note)
        return notes_by_date
