from django.http import HttpResponse

from django.template import loader

from datetime import datetime, timedelta

from .forms import ScheduleItemForm, ToDoItemForm, ToDoItem
from .models.appmodels import Day, ScheduleItem, ToDoList
from .utils import DaySchedule, relevant_time_dict


def day_view(request, datestr=None):
    """ Dashboard type view
        Provides static elements for presentation and set up for ajax calls

        Schedule table is rendered via ajax call to schedule_view
        To do list tables are rendered via ajax call to todo_list_view
    """
    template = loader.get_template('rolllist/day_schedule.html')

    if not datestr:
        target_date = datetime.today()
        datestr = '{0:%Y%m%d}'.format(target_date)
    else:
        target_date = datetime.strptime(datestr, "%Y%m%d").date()

    target_day, target_day_created = Day.get_or_create(date=target_date)

    context = {
        'datestr': datestr,
        'day': target_day
    }

    return HttpResponse(template.render(context, request))


def schedule_view(request, datestr):
    """ View providing the time interval schedule for a given day
    """
    template = loader.get_template('rolllist/schedule_table.html')
    target_date = datetime.strptime(datestr, "%Y%m%d").date()
    target_day, target_day_created = Day.get_or_create(date=target_date)
    day_schedule = DaySchedule(target_day, relevant_time_dict)

    context = {
        'datestr': datestr,
        'day': target_day,
        'day_schedule': day_schedule,
    }

    return HttpResponse(template.render(context, request))


def todo_list_view(request, datestr):
    """ View providing the to do lists for a given day
    """
    template = loader.get_template('rolllist/todo_list_table.html')
    target_date = datetime.strptime(datestr, "%Y%m%d").date()
    target_day, target_day_created = Day.get_or_create(date=target_date)

    previous_day_date = target_day.date - timedelta(days=1)
    previous_day, previous_created = Day.get_or_create(date=previous_day_date)

    todo_list, created = ToDoList.get_or_create(day=target_day)
    yesterday_to_do_list, created = ToDoList.get_or_create(day=previous_day)

    context = {
        'datestr': datestr,
        'todo_list': todo_list,
        'yesterday_to_do_list': yesterday_to_do_list,
    }
    return HttpResponse(template.render(context, request))


def add_schedule_item_form(request, start_time_int=None, datestr=None):
    """ Handler for add schedule item form
    """
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
            return HttpResponse()
        else:
            context = {'form': form}
            return HttpResponse(template.render(context, request))

    else:
        init_values = {}
        if start_time_int:
            init_values['start_time'] = relevant_time_dict[start_time_int]
            init_values['end_time'] = relevant_time_dict[start_time_int + 1]

        form = ScheduleItemForm(initial=init_values)
        context = {'form': form}
        return HttpResponse(template.render(context, request))


def delete_schedule_item(request, item_id):
    """ Delete schedule item of given ID """
    item = ScheduleItem.objects.get(pk=item_id)
    item.delete()
    return HttpResponse()


def add_to_do_item_form(request, list_id=None):
    """ Handler for add to do item form
    """
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
            return HttpResponse()
        else:
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        form = ToDoItemForm()
        context = {'form': form}
        return HttpResponse(template.render(context, request))


def rollover_todo(request, datestr):
    """ Handles copying incomplete items from previous day to day of given datestr
    """
    target_day = Day.objects.get(date=datetime.strptime(datestr, "%Y%m%d").date())
    previous_day_date = target_day.date - timedelta(days=1)
    source_day = Day.objects.get(date=previous_day_date)
    source_list, created = ToDoList.get_or_create(day=source_day)
    new_list, created = ToDoList.get_or_create(day=target_day)

    for item in source_list.todoitem_set.filter(completed=False).all():
        new_item = ToDoItem(title=item.title, to_do_list=new_list)
        new_item.save()
    return HttpResponse()


def delete_todo_item(request, item_id):
    """ Delete to do item of given ID """
    item = ToDoItem.objects.get(pk=item_id)
    item.delete()
    return HttpResponse()


def complete_todo_item(request, item_id):
    """ Set completed status on to do item of given ID """
    item = ToDoItem.objects.get(pk=item_id)
    item.completed = True
    item.save()
    return HttpResponse()


def revert_todo_item(request, item_id):
    """ Revert completed status on to do item of given ID """
    item = ToDoItem.objects.get(pk=item_id)
    item.completed = False
    item.save()
    return HttpResponse()
