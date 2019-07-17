from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse

from rolllistuser.forms import CreateUserForm, LoginUserForm, EditUserProfileForm


def create_init_view(request):
    template = loader.get_template('rolllist/session/user_init.html')
    context = {'create_form': CreateUserForm, 'login_form': LoginUserForm}
    return HttpResponse(template.render(context, request))


def login_handler(request):
    template = loader.get_template('rolllist/session/login.html')
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
                    messages.error(request, 'Invalid password.')
                    return HttpResponse(template.render(context, request))
            except Exception:
                context = {'login_form': form}
                messages.error(request, 'Invalid email.')
                return HttpResponse(template.render(context, request))

    else:
        context = {'login_form': LoginUserForm}
        return HttpResponse(template.render(context, request))


def logout_handler(request):
    logout(request)
    return redirect(reverse('login_handler'))


def create_handler(request):
    template = loader.get_template('rolllist/session/create.html')
    if request.POST:
        data = request.POST.copy()
        form = CreateUserForm(data)
        if form.is_valid():
            clean_data = form.cleaned_data.copy()
            if clean_data['password'] == clean_data['verify_password']:
                user_data = {
                    'email': clean_data['email'],
                    'username': clean_data['email'],
                    'password': clean_data['password']
                }
                try:
                    new_user = User.objects.create_user(
                        **user_data
                    )
                    login(request, new_user)
                    return redirect(reverse('dashboard'))
                except IntegrityError:
                    messages.error(
                        request,
                        'This email address is already in use.'
                    )
            else:
                messages.error(
                    request,
                    'Passwords do not match, please correct this and try again.'
                )
        else:
            if form.errors:
                errors = form.errors
            else:
                errors = ['invalid request, try again']
            template = loader.get_template('rolllist/session/create.html')
            context = {'create_form': form, 'errors': errors}
            return HttpResponse(template.render(context, request))

        form = CreateUserForm(data)
        context = {'create_form': form}
        return HttpResponse(template.render(context, request))
    else:
        form = CreateUserForm()
        context = {'create_form': form}
        return HttpResponse(template.render(context, request))


@login_required(login_url='login/')
def user_profile(request):
    user = request.user
    template = loader.get_template('rolllist/session/edit_user_profile.html')
    if request.POST:
        data = request.POST.copy()
        form = EditUserProfileForm(data)
        password_valid = data.get('password') and user.check_password(data['password'])
        if form.is_valid and password_valid:
            errors = False
            reset_password = False
            if data.get('new_password1'):
                if data.get('new_password1') != data.get('new_password2'):
                    messages.error(request, 'New password and verify password must match.')
                    errors = True
                if not errors:
                    reset_password = True

            if not errors:

                user.rolllistuser.schedule_start_time = data['schedule_start_time']
                user.rolllistuser.schedule_end_time = data['schedule_end_time']
                user.rolllistuser.save()
                user.email = data['email']
                user.username = data['email']
                user.save()
                if reset_password:
                    user.set_password(data['new_password1'])
                    update_session_auth_hash(request, request.user)
                messages.success(request, 'Updated user information.')
            else:
                form = EditUserProfileForm(data)
                context = {'user': user, 'form': form}
                return HttpResponse(template.render(context, request))
        elif not password_valid:
            messages.error(
                request,
                'Current correct password required to make user profile changes.'
            )
        else:
            messages.warning(
                request,
                'An unkown error occurred while updating user information, please try again.'
            )

        form = EditUserProfileForm(data)
        context = {'user': user, 'form': form}
        return HttpResponse(template.render(context, request))

    else:
        init_data = {
            'email': user.email,
            'schedule_start_time': user.rolllistuser.schedule_start_time,
            'schedule_end_time': user.rolllistuser.schedule_end_time
        }
        form = EditUserProfileForm(initial=init_data)

    context = {'user': user, 'form': form}
    return HttpResponse(template.render(context, request))
