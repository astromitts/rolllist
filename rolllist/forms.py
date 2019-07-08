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

    make_recurring_0 = BooleanField(
        label='Monday',
        required=False,
    )

    make_recurring_1 = BooleanField(
        label='Tuesday',
        required=False,
    )

    make_recurring_2 = BooleanField(
        label='Wednesday',
        required=False,
    )

    make_recurring_3 = BooleanField(
        label='Thursday',
        required=False,
    )

    make_recurring_4 = BooleanField(
        label='Friday',
        required=False,
    )

    make_recurring_5 = BooleanField(
        label='Saturday',
        required=False,
    )

    make_recurring_6 = BooleanField(
        label='Sunday',
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
            'start_time_init',
            'end_time_init',
            'make_recurring_0',
            'make_recurring_1',
            'make_recurring_2',
            'make_recurring_3',
            'make_recurring_4',
            'make_recurring_5',
            'make_recurring_6',
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
            'recurrance_0',
            'recurrance_1',
            'recurrance_2',
            'recurrance_3',
            'recurrance_4',
            'recurrance_5',
            'recurrance_6',
        ]


class ToDoItemForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'priority', ]


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['content']
