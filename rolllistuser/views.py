from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse

from rolllistuser.forms import CreateUserForm, LoginUserForm


def create_init_view(request):
    template = loader.get_template('rolllist/user_init.html')
    context = {'create_form': CreateUserForm, 'login_form': LoginUserForm}
    return HttpResponse(template.render(context, request))


def login_handler(request):
    template = loader.get_template('rolllist/login.html')
    if request.POST:
        data = request.POST.copy()
        data['username'] = data['email']
        form = LoginUserForm(data)
        if form.is_valid():
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                context = {'login_form': form}
                context['error'] = 'invalid password or email'
                return HttpResponse(template.render(context, request))
    else:
        context = {'login_form': LoginUserForm}
        return HttpResponse(template.render(context, request))


def logout_handler(request):
    logout(request)
    return redirect(reverse('login_handler'))


def create_handler(request):
    if request.POST:
        data = request.POST.copy()
        form = CreateUserForm(data)
        if form.is_valid():
            new_user = User.objects.create_user(
                **form.cleaned_data
            )
            login(request, new_user)
            return redirect(reverse('dashboard'))
        else:
            template = loader.get_template('rolllist/create_user.html')
            context = {'create_form': form}
            return HttpResponse(template.render(context, request))

    return redirect(reverse('user_init'))
