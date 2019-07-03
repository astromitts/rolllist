from django.forms import (
    ModelForm,
    ChoiceField,
    BooleanField,
    CharField,
    HiddenInput,
)
from .models.appmodels import RecurringScheduleItem, ScheduleItem, ToDoItem, Note
from .utils import relevant_time_dict


class ScheduleItemForm(ModelForm):
    start_time = ChoiceField(
        choices=[(i, string) for i, string in relevant_time_dict.items()]
    )

    end_time = ChoiceField(
        choices=[(i, string) for i, string in relevant_time_dict.items()]
    )

    make_recurring = BooleanField(
        label='Set as Recurring',
        required=False,
    )

    start_time_init = CharField(widget=HiddenInput(), required=False)
    end_time_init = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = ScheduleItem
        fields = [
            'start_time',
            'end_time',
            'title',
            'location',
            'make_recurring',
            'start_time_init',
            'end_time_init',
        ]


class RecurringScheduleItemForm(ModelForm):
    start_time = ChoiceField(
        choices=[(i, string) for i, string in relevant_time_dict.items()]
    )

    end_time = ChoiceField(
        choices=[(i, string) for i, string in relevant_time_dict.items()]
    )

    start_time_init = CharField(widget=HiddenInput(), required=False)
    end_time_init = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = RecurringScheduleItem
        fields = [
            'start_time',
            'end_time',
            'title',
            'location',
            'start_time_init',
            'end_time_init',
        ]


class ToDoItemForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'priority', ]


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['content']
