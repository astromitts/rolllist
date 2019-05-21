from django.http import HttpResponse
from django.template import loader

from datetime import datetime

from .models import Day, DaySchedule, time_options_strings


def today_view(request):
    template = loader.get_template('timelord/day_schedule.html')
    try:
        today_day = Day.objects.get(date=datetime.today())
    except:
        return HttpResponse('cant find today')

    earliest_time_index = time_options_strings.index('8:00 AM')
    latest_time_index = time_options_strings.index('6:30 PM')
    relevant_time_dict = {
        i: time_options_strings[i] for i in range(earliest_time_index, latest_time_index + 1)
    }

    day_schedule = DaySchedule(today_day, relevant_time_dict)

    context = {
        'day': today_day,
        'day_schedule': day_schedule,
        'schedule_items': today_day.scheduleitem_set.all(),
        'todo_items': today_day.todoitem_set.all(),
    }

    return HttpResponse(template.render(context, request))
