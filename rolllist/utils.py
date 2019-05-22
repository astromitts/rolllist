from django.db import models

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

# TODO move this to a user preferences
earliest_time_index = time_options_strings.index('8:00 AM')
latest_time_index = time_options_strings.index('6:30 PM')
relevant_time_dict = {
    i: time_options_strings[i] for i in range(earliest_time_index, latest_time_index + 1)
}


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
                models.Q(start_time=i) |
                (models.Q(start_time__lt=i) & models.Q(end_time__gt=i))
            ).all()
            self.time_intervals.append(this_interval)
