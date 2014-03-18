from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import MofficeUser

from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page'))

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email and not password:
            context = {"form_message": {"error": "Invalid login", "message": "All fields required"}}
            return render(request, 'login.html', context)

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.POST.get('next')
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(reverse('services_page'))
            else:
                context = {"form_message": {"error": "Invalid login", "message": "Disabled account"}}
                return render(request, 'login.html', context)

        else:
            context = {"form_message": {"error": "Invalid login", "message": "Invalid email or password"}}
            return render(request, 'login.html', context)

    else:
        context = {"next": request.GET.get('next')}
        return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))

def signup_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page'))

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email and not password:
            context = {"form_message": {"error": "Signup error", "message": "All fields required"}}
            return render(request, 'signup.html', context)

        user = MofficeUser()

        try:
            validate_email(email)

        except ValidationError:
            context = {"form_message": {"error": "Signup error", "message": "Enter a valid email address"}}
            return render(request, 'signup.html', context)
            
        user.email = email
        user.set_password(password)

        try:
            user.save()

        except IntegrityError:
            context = {"form_message": {"error": "Signup error", "message": "Email already exists."}}
            return render(request, 'signup.html', context)

        context = {"form_message": {"error": "Signup successful", "message": "We have sent confirmation email to you. Please, check."}}
        return render(request, 'signup.html', context)
        return HttpResponseRedirect(reverse('services_page'))
            

    else:
        return render(request, 'signup.html')

def forgot_password_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page'))

    if request.method == "POST":
        email = request.POST.get('email')

        if not email:
            context = {"form_message": {"error": "Signup error", "message": "Give us your email address"}}
            return render(request, 'forgot_password.html', context)

        #TODO
        #Password reset email send

        context = {"form_message": {"error": "Password reset successful", "message": "We have sent password reset link to you."}}
        return render(request, 'forgot_password.html', context)
            

    else:
        return render(request, 'forgot_password.html')


@login_required
def index_page(request):
    return HttpResponseRedirect(reverse('services_page'))

@login_required
def services_page(request):
    return render(request, 'services.html')

@login_required
def account_page(request):
    return render(request, 'account.html')

@login_required
def billing_page(request):
    return render(request, 'billing.html')

@login_required
def support_page(request):
    return render(request, 'support.html')

@login_required
def feedback_page(request):
    return render(request, 'feedback.html')

@login_required
def payment_page(request):
    return render(request, 'payment.html')

@login_required
def security_settings_page(request):
    return render(request, 'security_settings.html')

@login_required
def service_add_page(request):
    return render(request, 'service_add.html')

@login_required
def ticket_add_page(request):
    return render(request, 'ticket_add.html')
