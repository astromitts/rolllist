from django.forms import ModelForm, ChoiceField, BooleanField
from .models.appmodels import ScheduleItem, ToDoItem
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

    class Meta:
        model = ScheduleItem
        fields = ['start_time', 'end_time', 'title', 'location', 'make_recurring']


class ToDoItemForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title']
