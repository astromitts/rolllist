from django.forms import (
    ModelForm,
    Form,
    PasswordInput,
    EmailField,
    ChoiceField,
    CharField,
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

    verify_password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password', 'verify_password']
        widgets = {
            'password': PasswordInput(),
            'verify_password': PasswordInput(),
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

    new_password1 = CharField(widget=PasswordInput(), required=False)
    new_password2 = CharField(widget=PasswordInput(), required=False)
    password = CharField(widget=PasswordInput())

    class Meta:
        fields = [
            'email',
            'schedule_start_time',
            'schedule_end_time',
            'new_password1',
            'new_password2',
            'password'
        ]
        widgets = {
            'new_password1': PasswordInput(),
            'new_password2': PasswordInput(),
            'password': PasswordInput(),
        }
