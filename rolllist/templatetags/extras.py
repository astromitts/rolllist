from django import template
from rolllist.utils import relevant_time_dict

register = template.Library()


@register.filter
def set_row_class(timestr):
    if ':30' in timestr:
        return 'hour'
    return 'halfhour'


@register.filter
def time_display_str(int_id):
    return relevant_time_dict.get(int_id)
