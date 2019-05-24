from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User


class LoginUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': PasswordInput(),
        }


class CreateUserForm(LoginUserForm):

    pass
