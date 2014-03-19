from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Account, BaseService, AccountService

from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@login_required
def index_page(request):
    return HttpResponseRedirect(reverse('services_page'))

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

        if Account.objects.filter(email=email).count():
            context = {"form_message": {"error": "Signup error", "message": "Email already exists.", "type": "danger"}}
            return render(request, 'signup.html', context)

        if not email and not password:
            context = {"form_message": {"error": "Signup error", "message": "All fields required.", "type": "danger"}}
            return render(request, 'signup.html', context)


        try:
            validate_email(email)

        except ValidationError:
            context = {"form_message": {"error": "Signup error", "message": "Enter a valid email address.", "type": "danger"}}
            return render(request, 'signup.html', context)
            

        try:
            user = Account()
            user.email = email
            user.set_password(password)
            user.save()

        except:
            context = {"form_message": {"error": "Signup error", "message": "Internal server error.", "type": "danger"}}
            return render(request, 'signup.html', context)

        context = {"form_message": {"error": "Signup successful", "message": "Activation link sent.", "type": "success"}}
        return render(request, 'signup.html', context)
            

    else:
        return render(request, 'signup.html')


def forgot_password_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page'))

    if request.method == "POST":
        email = request.POST.get('email')

        if not email:
            context = {"form_message": {"error": "Password reset error", "message": "Give us your email address", "type": "danger"}}
            return render(request, 'forgot_password.html', context)

        try:
            this_user = Account.objects.get(email=email)
            #TODO
            #Password reset mail send
            # send_password_reset_link(email)

        except Account.DoesNotExist:
            context = {"form_message": {"error": "Password reset error", "message": "Email not found.", "type": "danger"}}
            return render(request, 'forgot_password.html', context)


        context = {"form_message": {"error": "Password reset successful", "message": "We have sent password reset link to you.", "type": "success"}}
        return render(request, 'forgot_password.html', context)
            

    else:
        return render(request, 'forgot_password.html')


@login_required
def services_page(request):
    current_user = Account.objects.get(email=request.user.email)
    context = { "services": current_user.services.all() }
    return render(request, 'services.html', context)

@login_required
def account_page(request):
    return render(request, 'account.html')

@login_required
def billing_page(request):
    return render(request, 'billing.html')

# @login_required
# def support_page(request):
#     return render(request, 'support.html')

@login_required
def settings_page(request):
    return render(request, 'settings.html')

@login_required
def feedback_page(request):
    return render(request, 'feedback.html')

@login_required
def payment_page(request):
    return render(request, 'payment.html')

@login_required
def security_page(request):
    return render(request, 'security.html')

@login_required
def notifications_page(request):
    return render(request, 'notifications.html')

@login_required
def service_add_page(request):
    if request.method == "POST":

        service = request.POST.get('service')
        users = request.POST.get('users')
        ip_address = request.POST.get('ip-address')
        hostname = request.POST.get('hostname')

        if not service:
            context = {"form_message": {"error": "Add service error", "message": "Choose plan to add", "type": "danger"}}
            return render(request, 'service_add.html', context)

        try:
            this_user = Account.objects.get(email=request.user.email)
            chosen_base_service = BaseService.objects.get(id=service)
            new_account_service = AccountService()
            new_account_service.service_type = chosen_base_service
            new_account_service.users = users
            new_account_service.ip_address = ip_address
            new_account_service.hostname = hostname
            new_account_service.save()

            this_user.services.add(new_account_service)

        except:
            context = {"form_message": {"error": "Add service error", "message": "Server error", "type": "danger"}}
            return render(request, 'service_add.html', context)

        return HttpResponseRedirect(reverse('index_page'))

    else:
        context = { "services": BaseService.objects.all()}
        return render(request, 'service_add.html', context)

@login_required
def ticket_add_page(request):
    return render(request, 'ticket_add.html')
