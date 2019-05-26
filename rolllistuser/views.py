from django.contrib.auth.models import User
from django.contrib.auth import login, logout
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
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.POST:
        data = request.POST.copy()
        form = LoginUserForm(data)
        if form.is_valid():
            try:
                user = User.objects.get(email=data['email'])
                if user.check_password(data['password']):
                    login(request, user)
                    return redirect(reverse('dashboard'))
                else:
                    context = {'login_form': form}
                    context['error'] = 'invalid password'
                    return HttpResponse(template.render(context, request))
            except:
                context = {'login_form': form}
                context['error'] = 'invalid email'
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
            if form.errors:
                errors = form.errors
            else:
                errors = ['invalid request, try again']
            template = loader.get_template('rolllist/create.html')
            context = {'create_form': form, 'errors': errors}
            return HttpResponse(template.render(context, request))

    template = loader.get_template('rolllist/create.html')
    form = CreateUserForm()
    context = {'create_form': form}
    return HttpResponse(template.render(context, request))
