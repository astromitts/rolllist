from django.http import HttpResponse
from django.shortcuts import redirect

from django.template import loader

from datetime import datetime

from .forms import ScheduleItemForm, ToDoItemForm, ToDoItem
from .models import Day, DaySchedule, ScheduleItem, relevant_time_dict


def day_view(request, datestr=None):
    template = loader.get_template('timelord/day_schedule.html')

    if not datestr:
        target_date = datetime.today()
        datestr = '{0:%Y%m%d}'.format(target_date)
    else:
        target_date = datetime.strptime(datestr, "%Y%m%d").date()

    try:
        today_day = Day.objects.get(date=target_date)
    except Day.DoesNotExist:
        today_day = Day(date=target_date)
        today_day.save()

    day_schedule = DaySchedule(today_day, relevant_time_dict)

    context = {
        'datestr': datestr,
        'day': today_day,
        'day_schedule': day_schedule,
        'todo_items': today_day.todoitem_set.all(),
    }

    return HttpResponse(template.render(context, request))


def add_item_form(request, start_time_int=None, datestr=None):
    template = loader.get_template('timelord/generic_form.html')

    if request.POST:
        data = request.POST.copy()
        target_day = Day.objects.get(date=datetime.strptime(datestr, "%Y%m%d").date())
        form = ScheduleItemForm(data)
        if form.is_valid():
            save_data = {
                'day': target_day,
                'start_time': data['start_time'],
                'end_time': data['end_time'],
                'title': data['title'],
                'location': data['location']
            }
            new_item = ScheduleItem(**save_data)
            new_item.save()
            return redirect('day_view', datestr=datestr)
        else:
            context = {'form_rendered_list': form.as_ul()}
            return HttpResponse(template.render(context, request))

    else:
        init_values = {}
        if start_time_int:
            init_values['start_time'] = relevant_time_dict[start_time_int]
            init_values['end_time'] = relevant_time_dict[start_time_int + 1]

        form = ScheduleItemForm(initial=init_values)
        context = {'form_rendered_list': form.as_ul()}
        return HttpResponse(template.render(context, request))


def delete_item(request, item_id):
    item = ScheduleItem.objects.get(pk=item_id)
    day = item.day
    item.delete()
    return redirect('day_view', datestr=day.url_str)


def delete_todo_item(request, item_id):
    item = ToDoItem.objects.get(pk=item_id)
    day = item.day
    item.delete()
    return redirect('day_view', datestr=day.url_str)


def add_to_do_item_form(request, datestr=None):
    template = loader.get_template('timelord/generic_form.html')
    if not datestr:
        target_date = Day.objects.get(date=datetime.today())
    else:
        target_date = Day.objects.get(date=datetime.strptime(datestr, "%Y%m%d").date())

    if request.POST:
        form = ToDoItemForm(request.POST)
        if form.is_valid:
            save_data = {
                'day': target_date,
                'title': request.POST['title'],
            }
            new_item = ToDoItem(**save_data)
            new_item.save()
            return redirect('day_view', datestr=datestr)
        else:
            context = {'form_rendered_list': form.as_ul()}
            return HttpResponse(template.render(context, request))
    else:
        form = ToDoItemForm()
        context = {'form_rendered_list': form.as_ul()}
        return HttpResponse(template.render(context, request))
