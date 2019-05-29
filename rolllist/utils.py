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
relevant_keys = [i for i in relevant_time_dict.keys()]


def get_relevant_time_id(search_time):
    for _id, _val in relevant_time_dict.items():
        if _val == search_time:
            return _id


class TimeInterval(object):
    """ Helper object for organizing data about a time interval
    """
    def __init__(self, index, start_string, end_string):
        self.index = index
        self.start_string = start_string
        self.end_string = end_string
        self.items = []
        if index == relevant_keys[-1]:
            self.next_index = None
        else:
            self.next_index = index + 1


class DaySchedule(object):
    """ Helper object for organizing scheduled items by time interval
    """
    def __init__(self, day, relevant_time_dict, user):
        self.day = day
        self.time_intervals = []

        for i, string in relevant_time_dict.items():
            this_interval = TimeInterval(
                i,
                time_options_strings[i],
                time_options_strings[i + 1]
            )

            this_interval.items = day.scheduleitem_set.filter(
                models.Q(start_time=i) |
                (models.Q(start_time__lt=i) & models.Q(end_time__gt=i))
            ).filter(user=user).all()
            self.time_intervals.append(this_interval)


class DayScheduleDeux(object):
    """
        [
            8:00 AM items: None,
            8:30 AM items: [
                (
                    id
                    title
                    location
                    start time id
                    end time id
                    start time display
                    end time display
                    interval count (end_time - start_time)
                    is recurring
                ),
            ],
            9:00 AM items: None
            9:30 AM items: [
                (
                    id
                    title
                    location
                    start time id
                    end time id
                    start time display
                    end time display
                    interval count (end_time - start_time)
                    is recurring
                ),
                (
                    id
                    title
                    location
                    start time id
                    end time id
                    start time display
                    end time display
                    interval count (end_time - start_time)
                    is recurring
                ),
            ],
            ...
        ]
    """
    def _organize_by_time(self, all_items):
        time_dict = {}
        for item in all_items:
            if not time_dict.get(item.start_time):
                time_dict[item.start_time] = []
            item_data = {
                'item': item,
                'interval_count': item.end_time - item.start_time
            }
            time_dict[item.start_time].append(item_data)
        return time_dict

    def __init__(self, day, user):
        self.day = day
        self.time_intervals = []

        self.all_items = day.get_schedule_items(user)
        items_time_dict = self._organize_by_time(self.all_items)
        self.items_by_time = {i.start_time: i for i in self.all_items}
        self.schedule = []
        for i, string in relevant_time_dict.items():
            data = {
                'start_time_display': string,
                'int_id': i,
                'items': None,
            }
            if i in items_time_dict:
                data['items'] = items_time_dict[i]
            self.schedule.append(data)
