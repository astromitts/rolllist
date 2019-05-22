from django.http import HttpResponse
from django.shortcuts import redirect

from django.template import loader

from datetime import datetime, timedelta

from .forms import ScheduleItemForm, ToDoItemForm, ToDoItem
from .models.appmodels import Day, ScheduleItem, ToDoList
from .utils import DaySchedule, relevant_time_dict


def day_view(request, datestr=None):
    template = loader.get_template('rolllist/day_schedule.html')

    if not datestr:
        target_date = datetime.today()
        datestr = '{0:%Y%m%d}'.format(target_date)
    else:
        target_date = datetime.strptime(datestr, "%Y%m%d").date()

    target_day, target_day_created = Day.get_or_create(date=target_date)

    previous_day_date = target_day.date - timedelta(days=1)
    previous_day, previous_created = Day.get_or_create(date=previous_day_date)

    if target_day_created:
        ScheduleItem.rollover_recurring_items(target_day)

    day_schedule = DaySchedule(target_day, relevant_time_dict)

    todo_list = ToDoList.get_or_create(target_day)
    yesterday_to_do_list = ToDoList.get_or_create(previous_day)

    context = {
        'datestr': datestr,
        'day': target_day,
        'day_schedule': day_schedule,
        'todo_list': todo_list,
        'yesterday_to_do_list': yesterday_to_do_list,
    }

    return HttpResponse(template.render(context, request))


def add_item_form(request, start_time_int=None, datestr=None):
    template = loader.get_template('rolllist/generic_form.html')

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
                'location': data['location'],
                # 'recurring': data['recurring'] == 'on',
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


def add_to_do_item_form(request, list_id=None):
    template = loader.get_template('rolllist/generic_form.html')
    if request.POST:
        form = ToDoItemForm(request.POST)
        to_do_list = ToDoList.objects.get(pk=list_id)
        if form.is_valid:
            save_data = {
                'to_do_list': to_do_list,
                'title': request.POST['title'],
            }
            new_item = ToDoItem(**save_data)
            new_item.save()
            return redirect('day_view', datestr=to_do_list.day.url_str)
        else:
            context = {'form_rendered_list': form.as_ul()}
            return HttpResponse(template.render(context, request))
    else:
        form = ToDoItemForm()
        context = {'form_rendered_list': form.as_ul()}
        return HttpResponse(template.render(context, request))


def rollover_todo(request, datestr):
    target_day = Day.objects.get(date=datetime.strptime(datestr, "%Y%m%d").date())
    previous_day_date = target_day.date - timedelta(days=1)
    source_day = Day.objects.get(date=previous_day_date)
    source_list = ToDoList.get_or_create(day=source_day)
    new_list = ToDoList.get_or_create(day=target_day)

    for item in source_list.todoitem_set.filter(completed=False).all():
        new_item = ToDoItem(title=item.title, to_do_list=new_list)
        new_item.save()
    return redirect('day_view', datestr=target_day.url_str)


def delete_todo_item(request, item_id):
    item = ToDoItem.objects.get(pk=item_id)
    day = item.to_do_list.day
    item.delete()
    return redirect('day_view', datestr=day.url_str)


def complete_todo_item(request, item_id):
    item = ToDoItem.objects.get(pk=item_id)
    day = item.to_do_list.day
    item.completed = True
    item.save()
    return redirect('day_view', datestr=day.url_str)


def revert_todo_item(request, item_id):
    item = ToDoItem.objects.get(pk=item_id)
    day = item.to_do_list.day
    item.completed = False
    item.save()
    return redirect('day_view', datestr=day.url_str)
