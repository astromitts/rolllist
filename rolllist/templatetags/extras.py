from django import template
from rolllist.utils import relevant_time_dict

register = template.Library()


@register.filter
def pdb(item):
    import pdb  # noqa
    pdb.set_trace()  # noqa


@register.filter
def message_class(message):
    """ Convert Django message types to CSS classes """
    if message.level_tag == 'error':
        return 'danger'
    else:
        return message.level_tag


@register.filter
def is_primary_time(time_string):
    """ Flag if a time string is a half hour or hour """
    return ':00' in time_string or ':30' in time_string


@register.filter
def get_dynamic_style(schedule_item, schedule):
    """ Produces dynamic positions for a given schedule item relative to the given schedule
    """
    table_position = schedule_item.start_time - schedule[0]['interval']
    styles = []
    if schedule_item.end_time - schedule_item.start_time == 1:
        styles.append('padding-top: .25rem;')
    else:
        styles.append('padding-top: {}rem;'.format((schedule_item.end_time - schedule_item.start_time) - 1))
    styles.append('top: {}rem;'.format(table_position * 2))
    styles.append('height: {}rem;'.format((schedule_item.end_time - schedule_item.start_time) * 2))
    return ' '.join(styles)


@register.filter
def set_schedule_item_display(item):
    html = '<span class="item-preview">{}</span><span class="item-full" id="item-full-{}">{}</span><button id="{}" class="item-expand">...</button>'  # noqa
    rendered_html = html.format(
        item.title[0:18],
        item.pk,
        item.title[19:],
        item.pk
    )
    return rendered_html


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
