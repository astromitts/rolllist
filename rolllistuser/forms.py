from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User


class LoginUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
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
