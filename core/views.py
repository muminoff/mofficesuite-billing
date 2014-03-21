from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Account, Service, Plan, ActivationToken, Invoice
from core.helper import send_activation_token, send_reset_password, generate_random_password

from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from decimal import Decimal


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
            context = {"form_message": {"error": "Invalid login", "message": "All fields required", "type": "danger"}}
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
                context = {"form_message": {"error": "Invalid login", "message": "Account not activated.", "type": "danger"}}
                return render(request, 'login.html', context)

        else:
            context = {"form_message": {"error": "Invalid login", "message": "Invalid email or password", "type": "danger"}}
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
            user.is_active = False
            user.save()
            token = ActivationToken(email=email)
            token.save()
            send_activation_token(request, token)

        except Exception as e:
            context = {"form_message": {"error": "Signup error", "message": "Cannot activate account. Contact support team.", "type": "danger"}}
            return render(request, 'signup.html', context)

        context = {"form_message": {"error": "Signup successful", "message": "Activation link sent.", "type": "success"}}
        return render(request, 'login.html', context)
            

    else:
        return render(request, 'signup.html')


def activate_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page'))

    if request.method == "GET":
        token = request.GET.get('token', '')

        if not token:
            return render(request, 'activate.html')

        if not ActivationToken.objects.filter(token=token).count():
            context = {"form_message": {"error": "Activation error", "message": "<h3>Invalid activation code.</h3>", "type": "danger"}}
            return render(request, 'activate.html', context)

        try:
            this_token = ActivationToken.objects.get(token=token)
            this_email = this_token.email
            this_user = Account.objects.get(email=this_email)
            this_user.is_active = True
            this_user.save()
            this_token.delete()

        except:
            context = {"form_message": {"error": "Activation error", "message": "<h3>Cannot activate account. Contact support team.</h3>", "type": "danger"}}
            return render(request, 'activate.html', context)

        context = {"form_message": {"error": "Activation successful", "message": "<h3>Account activated. You can now login.</h3>", "type": "success"}}
        return render(request, 'activate.html', context)

    else:
        return HttpResponseRedirect(reverse('login_page'))


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
            new_password = generate_random_password()
            this_user.set_password(new_password)
            this_user.save()
            send_reset_password(email, new_password)

        except Account.DoesNotExist:
            context = {"form_message": {"error": "Password reset error", "message": "Email not found.", "type": "danger"}}
            return render(request, 'forgot_password.html', context)


        context = {"form_message": {"error": "Password reset successful", "message": "Temporary password sent.", "type": "success"}}
        return render(request, 'forgot_password.html', context)
            

    else:
        return render(request, 'forgot_password.html')


@login_required
def services_page(request):
    current_user = Account.objects.get(email=request.user.email)
    context = { "services": current_user.services.all() }
    return render(request, 'services.html', context)

@login_required
def service_edit_page(request, id):

    if request.method == "POST":
        users = request.POST.get('users')

        if not users:
            context = {"form_message": {"error": "Service edit error", "message": "Users error", "type": "danger"}}
            return render(request, 'service_edit.html', context)

        try:
            this_user = Account.objects.get(email=email)
            #TODO
            #Password reset mail send
            # send_password_reset_link(email)

        except Account.DoesNotExist:
            context = {"form_message": {"error": "Password reset error", "message": "Email not found.", "type": "danger"}}
            return render(request, 'forgot_password.html', context)


        context = {"form_message": {"error": "Password reset successful", "message": "Password reset link sent.", "type": "success"}}
        return render(request, 'forgot_password.html', context)
            

    else:
        return render(request, 'forgot_password.html')

@login_required
def account_page(request):
    return render(request, 'account.html')

@login_required
def deactivate_page(request):
    if request.method == "POST":

        try:
            this_user = Account.objects.get(id=request.user.id)
            this_user.delete()

        except Exception as e:
            context = {"form_message": {"error": "Moffice Suite", "message": "Your account has been fully deactivated. Thanks for using Moffice Suite!", "type": "info"}}
            return render(request, 'login.html', context)

        context = {"form_message": {"error": "Moffice Suite", "message": "Your account has been <strong>FULLY DEACTIVATED</strong>. Thanks for using Moffice Suite!", "type": "warning"}}
        return render(request, 'login.html', context)

    else:
        return render(request, 'deactivate.html')

@login_required
def billing_page(request):
    context = { "invoices": Invoice.objects.filter(account=request.user) }
    return render(request, 'billing.html', context)

@login_required
def settings_page(request):
    if request.method == "POST":

        first = request.POST.get('first')
        last = request.POST.get('last')
        address = request.POST.get('address')
        company = request.POST.get('company')
        phone = request.POST.get('phone')

        try:
            this_user = Account.objects.get(id=request.user.id)
            this_user.first_name = first
            this_user.last_name = last
            this_user.company_address = address
            this_user.company_name = company
            this_user.phone_number = phone
            this_user.save()

        except Exception as e:
            context = {"form_message": {"error": "Settings error", "message": str(e), "type": "danger"}}
            return render(request, 'settings.html', context)

        # context = {"form_message": {"error": "Settings", "message": "Settings has been updated.", "type": "success"}}
        # return render(request, 'settings.html', context)
        return HttpResponseRedirect(reverse('settings_page'))

    else:
        return render(request, 'settings.html')

@login_required
def feedback_page(request):
    if request.method == "POST":

        subject = request.POST.get('subject')
        feedback = request.POST.get('feedback')

        if not subject or not feedback:
            context = {"form_message": {"error": "Feedback error", "message": "Write subject and feedback.", "type": "danger"}}
            return render(request, 'feedback.html', context)

        #TODO
        # send_feedback_via_mail
        try:
            pass

        except Exception as e:
            context = {"form_message": {"error": "Feedback error", "message": str(e), "type": "danger"}}
            return render(request, 'settings.html', context)

        context = {"form_message": {"error": "Feedback", "message": "Feedback sent. Thank you.", "type": "success"}}
        return render(request, 'feedback.html', context)

    else:
        return render(request, 'feedback.html')

@login_required
def payment_page(request):
    if request.method == "POST":

        amount = request.POST.get('amount')

        if not amount:
            context = {"form_message": {"error": "Payment error", "message": "No amount given.", "type": "danger"}}
            return render(request, 'payment.html', context)

        try:
            this_user = Account.objects.get(email=request.user.email)
            this_user.balance += Decimal(amount)
            this_user.save()

        except Exception as e:
            context = {"form_message": {"error": "Payment error", "message": str(e), "type": "danger"}}
            return render(request, 'payment.html', context)

        context = {"form_message": {"error": "Payment successful", "message": "Payment has been proceeded. Check your balance now.", "type": "success"}}
        return render(request, 'payment.html', context)

    else:
        return render(request, 'payment.html')

@login_required
def security_page(request):
    if request.method == "POST":

        current_password = request.POST.get('current')
        new_password = request.POST.get('password')
        new_password2 = request.POST.get('password2')

        if not current_password:
            context = {"form_message": {"error": "Security error", "message": "You must enter your current password.", "type": "danger"}}
            return render(request, 'security.html', context)

        if not new_password and not new_password2:
            context = {"form_message": {"error": "Security error", "message": "You must enter your new password.", "type": "danger"}}
            return render(request, 'security.html', context)

        if new_password != new_password2:
            context = {"form_message": {"error": "Security error", "message": "New passwords don't match.", "type": "danger"}}
            return render(request, 'security.html', context)

        try:
            user = authenticate(email=request.user.email, password=current_password)
            if user is None:
                context = {"form_message": {"error": "Security error", "message": "Invalid password", "type": "danger"}}
                return render(request, 'security.html', context)

            user.set_password(new_password)
            user.save()

        except Exception as e:
            context = {"form_message": {"error": "Security error", "message": str(e), "type": "danger"}}
            return render(request, 'security.html', context)

        context = {"form_message": {"error": "Security error", "message": "Password changed.", "type": "success"}}
        return render(request, 'security.html', context)

    else:
        return render(request, 'security.html')

@login_required
def notifications_page(request):
    return render(request, 'notifications.html')

@login_required
def service_add_page(request):
    if request.method == "POST":

        plan = request.POST.get('plan')
        users = request.POST.get('users')
        ip_address = request.POST.get('ip-address')
        hostname = request.POST.get('hostname')

        if not plan:
            context = {
                    "plans": Plan.objects.all(),
                    "form_message": {"error": "Add service error", "message": "No plan selected.", "type": "danger"}
                    }
            return render(request, 'service_add.html', context)

        if not hostname:
            context = {
                    "plans": Plan.objects.all(),
                    "form_message": {"error": "Add service error", "message": "No hostname given.", "type": "danger"}
                    }
            return render(request, 'service_add.html', context)

        if Service.objects.filter(hostname=hostname).count():
            context = {
                    "plans": Plan.objects.all(),
                    "form_message": {"error": "Add service error", "message": "Hostname \"%s\" already taken. Choose another one." % hostname, "type": "danger"}
                    }
            return render(request, 'service_add.html', context)

        try:
            this_user = Account.objects.get(id=request.user.id)
            chosen_base_plan = Plan.objects.get(id=plan)
            new_account_service = Service()
            new_account_service.plan = chosen_base_plan
            new_account_service.users = users
            new_account_service.ip_address = ip_address
            new_account_service.hostname = hostname
            new_account_service.status = 'activated'
            new_account_service.save()

            this_user.services.add(new_account_service)

        except Exception as e:
            context = {"form_message": {"error": "Add service error", "message": str(e), "type": "danger"}}
            return render(request, 'service_add.html', context)

        return HttpResponseRedirect(reverse('index_page'))

    else:
        context = { "plans": Plan.objects.all()}
        return render(request, 'service_add.html', context)
