from django.db import models
from datetime import datetime


time_options_strings = []

time_options_strings.append('12:00 AM')
time_options_strings.append('12:30 AM')

for i in range(1, 12):
    time_options_strings.append('%s:00 AM' % i)
    time_options_strings.append('%s:30 AM' % i)

time_options_strings.append('12:00 PM')
time_options_strings.append('12:30 PM')

for i in range(1, 12):
    time_options_strings.append('%s:00 PM' % i)
    time_options_strings.append('%s:30 PM' % i)

earliest_time_index = time_options_strings.index('8:00 AM')
latest_time_index = time_options_strings.index('6:30 PM')
relevant_time_dict = {
    i: time_options_strings[i] for i in range(earliest_time_index, latest_time_index + 1)
}


class Day(models.Model):
    date = models.DateField(default=datetime.today)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return '{0:%B %d %Y}'.format(self.date)


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


class ToDoItem(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return '%s (%s)' % (self.title, self.day)


class TimeInterval(object):
    def __init__(self, index, start_string, end_string):
        self.index = index
        self.start_string = start_string
        self.end_string = end_string
        self.items = []


class DaySchedule(object):
    def __init__(self, day, relevant_time_dict):
        self.day = day
        self.time_intervals = []

        for i, string in relevant_time_dict.items():
            this_interval = TimeInterval(
                i, time_options_strings[i], time_options_strings[i + 1]
            )
            this_interval.items = day.scheduleitem_set.filter(
                models.Q(start_time=i) | models.Q(end_time=i) |
                (models.Q(start_time__lt=i) & models.Q(end_time__gt=i))
            ).all()
            self.time_intervals.append(this_interval)
