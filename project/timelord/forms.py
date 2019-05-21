from django.forms import ModelForm, ChoiceField
from .models import ScheduleItem, ToDoItem, relevant_time_dict


class ScheduleItemForm(ModelForm):
    start_time = ChoiceField(
        choices=[(i, string) for i, string in relevant_time_dict.items()]
    )

    end_time = ChoiceField(
        choices=[(i, string) for i, string in relevant_time_dict.items()]
    )

    class Meta:
        model = ScheduleItem
        fields = ['start_time', 'end_time', 'title', 'location']


class ToDoItemForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title']
