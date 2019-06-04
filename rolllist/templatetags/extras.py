from django import template
from rolllist.utils import relevant_time_dict
from rolllist.models.appmodels import RecurringScheduleItem

register = template.Library()


@register.filter
def set_row_class(timestr):
    if ':30' in timestr:
        return 'solid'
    return 'dashed'


@register.filter
def time_display_str(int_id):
    return relevant_time_dict.get(int_id)


@register.filter
def is_recurring_item(item):
    if isinstance(item, RecurringScheduleItem):
        return 1
    return 0


@register.filter
def format_timestamp_date(timestamp):
    return '{0:%m-%d-%Y}'.format(timestamp)


@register.filter
def format_timestamp_time(timestamp):
    return '{0:%I:%M %p}'.format(timestamp)
