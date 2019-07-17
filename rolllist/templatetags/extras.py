from django import template
from rolllist.utils import relevant_time_dict

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
    if item.recurrance:
        return 1
    return 0


@register.filter
def format_timestamp(timestamp):
    return '{0:%m-%d-%Y %I:%M %p}'.format(timestamp)


@register.filter
def set_alert_class(alert_tag):
    default = 'primary'
    alert_classes = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    }
    return alert_classes.get(alert_tag, default)
