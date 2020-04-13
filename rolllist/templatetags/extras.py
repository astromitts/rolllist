from django import template
from rolllist.utils import relevant_time_dict

register = template.Library()


@register.filter
def pdb(item):
    import pdb  # noqa
    pdb.set_trace()  # noqa


@register.filter
def message_class(message):
    if message.level_tag == 'error':
        return 'danger'
    else:
        return message.level_tag


@register.filter
def is_primary_time(time_string):
    return ':00' in time_string or ':30' in time_string


@register.filter
def get_dynamic_style(schedule_item, schedule):
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
def schedule_item_class(forloop, time_string):
    is_first = forloop['first']
    is_last = forloop['last']
    is_primary = is_primary_time(time_string)
    classes = ['booked-item']
    if is_first:
        classes.append('item-start')
        if is_primary:
            classes.append('item-start__primary')
        else:
            classes.append('item-start__secondary')
    if is_last:
        classes.append('item-end')
        if is_primary:
            classes.append('item-end__primary')
        else:
            classes.append('item-end__secondary')
    if not is_first and not is_last:
        classes.append('item-middle')
    return ' '.join(classes)


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
