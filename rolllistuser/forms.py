from django.forms import (
    ModelForm,
    Form,
    PasswordInput,
    EmailField,
    ChoiceField
)
from django.contrib.auth.models import User
from rolllist.utils import time_options_strings


class LoginUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': PasswordInput(),
        }


class CreateUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': PasswordInput(),
        }


class EditUserProfileForm(Form):
    email = EmailField()
    schedule_start_time = ChoiceField(
        choices=[
            (i, time_options_strings[i]) for i in range(0, len(time_options_strings))
        ]
    )
    schedule_end_time = ChoiceField(
        choices=[
            (i, time_options_strings[i]) for i in range(0, len(time_options_strings))
        ]
    )

    class Meta:
        fields = [
            'email',
            'schedule_start_time',
            'schedule_end_time'
        ]
