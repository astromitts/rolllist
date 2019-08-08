from django.forms import (
    ModelForm,
    Form,
    PasswordInput,
    EmailField,
    ChoiceField,
    CharField,
    BooleanField,
)
from django.contrib.auth.models import User
from rolllistuser.models import todo_style_choices
from rolllist.utils import time_options_strings


class LoginUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': PasswordInput(),
        }


class CreateUserForm(ModelForm):

    user_agreement = BooleanField(required=True)
    verify_password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['user_agreement', 'email', 'password', 'verify_password']
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

    todo_style = ChoiceField(choices=todo_style_choices)

    new_password1 = CharField(widget=PasswordInput(), required=False)
    new_password2 = CharField(widget=PasswordInput(), required=False)
    password = CharField(widget=PasswordInput())

    class Meta:
        fields = [
            'email',
            'schedule_start_time',
            'schedule_end_time',
            'todo_style',
            'password'
        ]
        widgets = {
            'password': PasswordInput(),
        }


class ChangePasswordUserForm(Form):
    new_password = CharField(widget=PasswordInput(), required=True)
    verify_password = CharField(widget=PasswordInput(), required=True)
    password = CharField(widget=PasswordInput(), required=True)

    class Meta:
        widgets = {
            'password': PasswordInput(),
            'new_password': PasswordInput(),
            'verify_password': PasswordInput(),
        }
