from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
# from django.urls import reverse
from django.template import loader

from datetime import datetime, timedelta

from .forms import (
    RecurringScheduleItemForm,
    ScheduleItemForm,
    ToDoItemForm,
    NoteForm
)

from .models.appmodels import (
    Day,
    ScheduleItem,
    RecurringScheduleItem,
    ToDoList,
    Note,
    ToDoItem
)
from rolllistuser.models import RollListUser
from .utils import DayScheduleDeux, _requested_recurrances


def get_user(request):
    user = User.objects.get(email=request.user.email)
    return RollListUser.objects.get(user=user)


def get_item(item_id, recurring):
    item = ScheduleItem.objects.get(pk=item_id)
    return item


def day_view(request, datestr=None):
    """ Dashboard type view
        Provides static elements for presentation and set up for ajax calls

        Schedule table is rendered via ajax call to schedule_view
        To do list tables are rendered via ajax call to todo_list_view
    """
    if request.user.is_authenticated:
        template = loader.get_template('rolllist/dashboard/dashboard.html')

        if not datestr:
            target_day, created = Day.get_or_create(date=datetime.today())
        else:
            target_day, created = Day.get_from_str(datestr)

        context = {
            'datestr': target_day.display_string,
            'day': target_day
        }
    else:
        template = loader.get_template('rolllist/about.html')
        context = {}

    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def schedule_view(request, datestr):
    """ View providing the time interval schedule for a given day
    """
    template = loader.get_template('rolllist/dashboard/schedule_table.html')
    target_date = datetime.strptime(datestr, "%Y%m%d").date()
    target_day, target_day_created = Day.get_or_create(date=target_date)

    day_schedule = DayScheduleDeux(target_day, get_user(request))

    context = {
        'datestr': datestr,
        'day': target_day,
        'day_schedule': day_schedule.schedule,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def note_view(request, datestr):
    """ View providing notes for a given day
    """
    template = loader.get_template('rolllist/dashboard/notes_table.html')
    target_date = datetime.strptime(datestr, "%Y%m%d").date()
    target_day, target_day_created = Day.get_or_create(date=target_date)
    notes = Note.objects.filter(day=target_day, user=get_user(request)).all()

    context = {
        'datestr': datestr,
        'day': target_day,
        'notes': notes,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def todo_list_view(request, datestr):
    """ View providing the to do lists for a given day
    """
    template = loader.get_template('rolllist/dashboard/todo_list_table.html')
    target_date = datetime.strptime(datestr, "%Y%m%d").date()
    target_day, target_day_created = Day.get_or_create(date=target_date)

    previous_day_date = target_day.date - timedelta(days=1)
    previous_day, previous_created = Day.get_or_create(date=previous_day_date)

    todo_list, created = ToDoList.get_or_create(
        day=target_day,
        user=get_user(request)
    )

    context = {
        'datestr': datestr,
        'todo_list': todo_list
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def add_schedule_item_form(request, start_time_int=None, datestr=None):
    """ Handler for add schedule item form
    """
    template = loader.get_template('rolllist/forms/schedule_item_form.html')

    if request.POST:
        data = request.POST.copy()
        data['start_time_init'] = data['start_time']
        data['end_time_init'] = data['end_time']
        target_day = Day.objects.get(
            date=datetime.strptime(datestr, "%Y%m%d").date()
        )
        form = ScheduleItemForm(data)
        if form.is_valid():
            save_data = {
                'start_time': data['start_time'],
                'end_time': data['end_time'],
                'title': data['title'],
                'location': data['location'],
                'user': get_user(request),
            }
            save_data['day'] = target_day
            # save it for today no matter what
            new_item = ScheduleItem(**save_data)

            # if they requested recurring, set it as recurring
            requested_recurrances = _requested_recurrances(data)
            if requested_recurrances:
                new_item, recurring_item = new_item.make_recurring(requested_recurrances)

            new_item.save()
            return HttpResponse()
        else:
            context = {'form': form}
            return HttpResponse(template.render(context, request))

    else:
        init_values = {}
        if start_time_int:
            init_values['start_time_init'] = start_time_int
            init_values['end_time_init'] = start_time_int + 1

        form = ScheduleItemForm(initial=init_values)
        context = {'form': form}
        return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def edit_schedule_item_form(request, item_id, recurring):
    """ Handler for edit schedule item form
    """
    template = loader.get_template('rolllist/forms/schedule_item_form.html')
    existing_item = get_item(item_id, recurring)

    if request.POST:
        data = request.POST.copy()
        form = ScheduleItemForm(data)
        if form.is_valid():
            existing_item.start_time = data['start_time']
            existing_item.end_time = data['end_time']
            existing_item.title = data['title']
            existing_item.location = data['location']

            # if they requested recurring, set it as recurring
            requested_recurrances = _requested_recurrances(data)
            if requested_recurrances:
                existing_item, recurring_item = existing_item.make_recurring(requested_recurrances)

            existing_item.save()

            return HttpResponse()
        else:
            context = {'form': form}
            return HttpResponse(template.render(context, request))

    else:
        init_values = {}
        init_values['start_time_init'] = existing_item.start_time
        init_values['end_time_init'] = existing_item.end_time
        form = ScheduleItemForm(instance=existing_item, initial=init_values)
        context = {'form': form}
        return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def delete_schedule_item_handler(request, item_id, recurring):
    """ Delete schedule item of given ID """
    item = get_item(item_id, recurring)

    if request.POST:
        if recurring:
            item.is_active = False
            item.save()
        else:
            item.delete()
        return HttpResponse()

    template = loader.get_template('rolllist/forms/generic_delete_form.html')
    if recurring:
        msg = "'%s' is a recurring event - Delete it for today only?" % item.title
    else:
        msg = 'Delete %s?' % item.title
    context = {
        'item': item,
        'message': msg,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def manage_recurring_items(request):
    """ Main dashboard-like view for managing all recurring item instances
    """
    user = get_user(request)
    recurring_items = RecurringScheduleItem.objects.filter(user=user)
    template = loader.get_template('rolllist/user_schedule/user_manage_recurring_items.html')
    context = {
        'recurring_items': recurring_items.all()
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def delete_recurring_item_handler(request, item_id):
    """ Handler for deleting a RecurringScheduleItem """
    target_item = RecurringScheduleItem.objects.get(pk=item_id)
    if request.POST:
        target_day, created = Day.get_or_create(date=datetime.today())
        target_item.delete_current_and_future(target_day)
        return HttpResponse()
    template = loader.get_template('rolllist/forms/generic_delete_form.html')
    context = {
        'item': target_item,
        'message': (
            'Deleting this recurring event will delete it from your schedule '
            'for today and all future dates. Confirm?'
        ),
        'submit_text': 'Confirm'
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def edit_recurring_item_handler(request, item_id):
    """ Handler for editing a RecurringScheduleItem """
    template = loader.get_template('rolllist/forms/schedule_item_form.html')
    target_item = RecurringScheduleItem.objects.get(pk=item_id)
    if request.POST:
        data = request.POST.copy()
        form = RecurringScheduleItemForm(data)
        if form.is_valid():
            target_day, created = Day.get_or_create(date=datetime.today())
            update_vars = {
                'start_time': data['start_time'],
                'end_time': data['end_time'],
                'title': data['title'],
                'location': data['location']
            }
            for i in range(0, 7):
                flag_name = 'recurrance_%s' % i
                set_value = data.get(flag_name, 'off') == 'on'
                if set_value:
                    update_vars[flag_name] = True
                else:
                    update_vars[flag_name] = False

            target_item.update_current_and_future(target_day, update_vars)

            return HttpResponse()
        else:
            context = {'form': form}
            return HttpResponse(target_item.render(context, request))

    else:
        init_values = {}
        init_values['start_time_init'] = target_item.start_time
        init_values['end_time_init'] = target_item.end_time
        form = RecurringScheduleItemForm(instance=target_item, initial=init_values)
        context = {'form': form}
        return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def add_to_do_item_form(request, list_id=None):
    """ Handler for add to do item form
    """
    template = loader.get_template('rolllist/forms/generic_form.html')
    if request.POST:
        form = ToDoItemForm(request.POST)
        to_do_list = ToDoList.objects.get(pk=list_id)
        if form.is_valid:
            save_data = {
                'to_do_list': to_do_list,
                'title': request.POST['title'],
                'priority': request.POST['priority']
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


@login_required(login_url='login/')
def edit_to_do_item_form(request, item_id=None):
    """ Handler for edit to do item form
    """
    template = loader.get_template('rolllist/forms/generic_form.html')
    to_do_item = ToDoItem.objects.get(pk=item_id)
    if request.POST:
        form = ToDoItemForm(request.POST)
        if form.is_valid:
            to_do_item.title = request.POST['title']
            to_do_item.priority = request.POST['priority']
            to_do_item.save()
            return HttpResponse()
        else:
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        form = ToDoItemForm(instance=to_do_item)
        context = {'form': form}
        return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def rollover_todo(request, datestr):
    """ Handles copying incomplete items from previous day to day of given datestr
    """
    target_day = Day.objects.get(
        date=datetime.strptime(datestr, "%Y%m%d").date()
    )
    source_list, created = ToDoList.get_or_create(
        day=target_day,
        user=request.user.rolllistuser
    )
    source_list.rollover_items()
    return HttpResponse()


@login_required(login_url='login/')
def delete_todo_item(request, item_id):
    """ Delete to do item of given ID """
    item = ToDoItem.objects.get(pk=item_id)

    if request.POST:
        item.delete()
        return HttpResponse()

    template = loader.get_template('rolllist/forms/generic_delete_form.html')
    context = {
        'item': item,
        'message': "Delete '%s'?" % item.title,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def complete_todo_item(request, item_id):
    """ Set completed status on to do item of given ID """
    item = ToDoItem.objects.get(pk=item_id)
    item.completed = True
    item.save()
    return HttpResponse()


@login_required(login_url='login/')
def revert_todo_item(request, item_id):
    """ Revert completed status on to do item of given ID """
    item = ToDoItem.objects.get(pk=item_id)
    item.completed = False
    item.save()
    return HttpResponse()


@login_required(login_url='login/')
def delete_note_form(request, note_id=None):
    """ Delete note item of given ID """
    note = Note.objects.get(pk=note_id)

    if request.POST:
        note.delete()
        return HttpResponse()

    template = loader.get_template('rolllist/forms/generic_delete_form.html')
    context = {
        'item': note,
        'message': 'Delete %s?' % note.content,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def edit_note_form(request, note_id=None, src=None):
    """ Handler for edit note form
    """
    template = loader.get_template('rolllist/user_notes/note_form.html')
    note = Note.objects.get(pk=note_id)
    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid:
            note.content = request.POST['content']
            note.save()
            if not src:
                return redirect('/%s/' % note.day.to_url_str)
            else:
                return redirect('/%s/' % src)
        else:
            context = {
                'form': form,
                'prefill_content': request.POST['content']
            }
            return HttpResponse(template.render(context, request))
    else:
        form = NoteForm(instance=note)
        context = {'form': form, 'prefill_content': note.content}
        return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def add_note_form(request, datestr=None, src=None):
    """ Handler for add note form
    """
    template = loader.get_template('rolllist/user_notes/note_form.html')
    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid:
            day, created = Day.get_from_str(datestr)
            note = Note(content=request.POST['content'], day=day, user=get_user(request))
            note.save()
            messages.success(request, 'Note added: %d' % note.id)
            if not src:
                return redirect('/%s/#notescontainer' % note.day.to_url_str)
            else:
                return redirect('/%s/' % src)
        else:
            context = {'form': form}
            return HttpResponse(template.render(context, request))
    else:
        form = NoteForm()
        context = {'form': form}
        return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def view_all_notes(request):
    """ View for listing all of a User's notes """
    user = get_user(request)
    template = loader.get_template('rolllist/user_notes/user_all_notes.html')
    notes = Note.get_all_for_user_by_day(user=user)
    today_day, created = Day.get_or_create(date=datetime.today())
    context = {
        'all_notes': notes,
        'today': today_day
    }
    return HttpResponse(template.render(context, request))
