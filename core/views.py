from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Account, Service, Plan, ActivationToken, ResetToken, Invoice, Notification
from core.helper import send_activation_token, send_reset_token, send_welcome_message, send_feedback, generate_random_password

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

        user = authenticate(email=email, password=password)
        if user is not None:

            if user.is_activated:
                login(request, user)
                next_page = request.POST.get('next')
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    # if request.user.is_staff:
                    #     logout(request)
                    #     context = {"form_message": {"title": "<span class=\"icon-caution\"></span> LOGIN ERROR", "message": "Admins not allowed :)", "type": "info", "animation": "animated fadeIn" }}
                    #     return render(request, 'login.html', context)

                    return HttpResponseRedirect(reverse('services_page'))
            else:
                context = {"form_message": {"title": "<span class=\"icon-caution\"></span> LOGIN ERROR", "message": "Account not activated.", "type": "warning", "animation": "animated shake" }}
                return render(request, 'login.html', context)

        else:
            context = {"form_message": {"title": "<span class=\"icon-caution\"></span> LOGIN ERROR", "message": "Invalid email or password.", "type": "danger", "animation": "animated shake" }}
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

        if Account.objects.filter(email=email).exists():
            context = {"form_message": {"title": "<span class=\"icon-caution\"></span> SIGNUP ERROR", "message": "Email already exists.", "type": "danger", "animation": "animated shake" }}
            return render(request, 'signup.html', context)

        if not email or not password:
            context = {"form_message": {"title": "<span class=\"icon-caution\"></span> SIGNUP ERROR", "message": "All fields are required.", "type": "danger", "animation": "animated shake" }}
            return render(request, 'signup.html', context)

        try:
            validate_email(email)

        except ValidationError:
            context = {"form_message": {"title": "<span class=\"icon-caution\"></span> SIGNUP ERROR", "message": "Enter a valid email address.", "type": "danger", "animation": "animated shake" }}
            return render(request, 'signup.html', context)
            
        try:
            user = Account()
            user.email = email
            user.set_password(password)
            user.is_activated = False
            user.save()
            Notification.objects.create(account=user, description="Account created.")
            token = ActivationToken(email=email)
            token.save()
            send_activation_token(request, token)
            Notification.objects.create(account=user, description="Activation mail sent.")

        except Exception as e:
            context = {"form_message": {"title": "<span class=\"icon-caution\"></span> SIGNUP ERROR", "message": "Cannot create account. Contact support team.<br/> DEBUG" + str(e), "type": "danger"}
                    }
            return render(request, 'signup.html', context)

        context = {"form_message": {"title": "<span class=\"icon-happy\"></span> SIGNUP SUCCESS", "message": " Activation mail sent.", "type": "success"}}
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
            this_user.is_activated = True
            this_user.save()
            this_token.delete()
            Notification.objects.create(account=this_user, description="Account activated.", status="success")
            send_welcome_message(this_email)

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
            token = ResetToken.objects.create(email=email)
            send_reset_token(request, token)
            this_account = Account.objects.get(email=email)
            Notification.objects.create(account=this_account, description="Password reset link set.", status="warning")

        except Account.DoesNotExist:
            context = {"form_message": {"error": "Password reset error", "message": "Email not found.", "type": "danger"}}
            return render(request, 'forgot_password.html', context)

        except Exception as e:
            context = {"form_message": {"error": "Password reset error", "message": "Cannot reset this account. Contact support team.", "type": "danger"}}
            return render(request, 'forgot_password.html', context)


        context = {"form_message": {"error": "Password reset link sent", "message": "Password reset link sent.", "type": "success"}}
        return render(request, 'forgot_password.html', context)
            

    else:
        return render(request, 'forgot_password.html')


def reset_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index_page'))

    if request.method == "GET":
        token = request.GET.get('token', '')

        if not token:
            return HttpResponseRedirect(reverse('login_page'))

        if not ResetToken.objects.filter(token=token).count():
            context = {"form_message": {"error": "Password reset error", "message": "Password reset link expired.", "type": "danger"}}
            return render(request, 'login.html', context)

        context = { "token": ResetToken.objects.get(token=token) }
        return render(request, 'reset.html', context)

    elif request.method == "POST":
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        token = request.POST.get('token')

        if not token:
            return HttpResponseRedirect(reverse('login_page'))

        if not ResetToken.objects.filter(token=token).count():
            context = {"form_message": {"error": "Password reset error", "message": "Password reset link expired.", "type": "danger"}}
            return render(request, 'login.html', context)

        if password != password2:
            context = {"form_message": {"error": "Password reset error", "message": "Passwords don't match.", "type": "danger"}}
            return render(request, 'reset.html', context)

        if not password or not password2:
            context = {"form_message": {"error": "Password reset error", "message": "All fields are required.", "type": "danger"}}
            return render(request, 'reset.html', context)

        try:
            this_token = ResetToken.objects.get(token=token)
            this_email = this_token.email
            this_account = Account.objects.get(email=this_email)
            this_account.set_password(password2)
            this_account.save()
            this_token.delete()
            Notification.objects.create(account=this_account, description="Password reset by request.", status="success")

        except:
            context = {"form_message": {"error": "Password reset error", "message": "Cannot reset this account. Contact support team.", "type": "danger"}}
            return render(request, 'reset.html', context)

        context = {"form_message": {"error": "Password reset successful", "message": "New password applied. You can now login.", "type": "success"}}
        return render(request, 'login.html', context)



@login_required
def services_page(request):
    return render(request, 'services.html')

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

        try:
            this_user = Account.objects.get(email=request.user.email)
            send_feedback(this_user, subject, feedback)

        except Exception as e:
            context = {"form_message": {"error": "Feedback error", "message": str(e), "type": "danger"}}
            return render(request, 'feedback.html', context)

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
            Notification.objects.create(account=this_user, description="$%s USD payment proceeded." % str(Decimal(amount)), status="success")

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
    context = { "notifications": Notification.objects.filter(account=request.user)[:5] }
    return render(request, 'notifications.html', context)


@login_required
def service_add_page(request):
    if request.method == "POST":

        plan = request.POST.get('plan')
        users = request.POST.get('users')
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
            new_service = Service()
            new_service.account = this_user
            new_service.plan = chosen_base_plan
            new_service.users = users
            new_service.hostname = hostname
            new_service.status = 'active'
            new_service.save()

            Notification.objects.create(account=this_user, description="New service \"%s\" added." % new_service.hostname, status="info")

        except Exception as e:
            context = {"form_message": {"error": "Add service error", "message": str(e), "type": "danger"}}
            return render(request, 'service_add.html', context)

        return HttpResponseRedirect(reverse('index_page'))

    else:
        if not request.user.has_balance():
            context = {"form_message": {"error": "Add service error", "message": "You cannot add service if your balance is below $1.", "type": "danger"} }
            return render(request, 'services.html', context)

        context = { "plans": Plan.objects.all()}
        return render(request, 'service_add.html', context)


@login_required
def service_edit_page(request, hostname):
    if request.method == "POST":

        users = request.POST.get('users')

        if not users:
            context = {
                    "plans": Plan.objects.all(),
                    "form_message": {"error": "Service error", "message": "No users given.", "type": "danger"}
                    }
            return render(request, 'service_edit.html', context)

        try:
            this_service = Service.objects.get(account=request.user, hostname=hostname)
            this_service.users = users
            this_service.save()
            Notification.objects.create(account=this_service.account, description="Service \"%s\" modified." % (this_service.hostname), status="info")

        except Exception as e:
            context = {
                    "form_message": {"error": "Service error", "message": str(e), "type": "danger"}
                    }
            return render(request, 'service_edit.html', context)

        return HttpResponseRedirect(reverse('index_page'))

    else:

        print '>>>>>>>>>>>>>>>>>', hostname
        if Service.objects.get(hostname=hostname).account != request.user:
            context = {
                    "plans": Plan.objects.all(),
                    "form_message": {"error": "Service error", "message": "Prohibited.", "type": "danger"}
                    }
            return render(request, 'service_edit.html', context)

        context = { "service": Service.objects.get(hostname=hostname) }
        return render(request, 'service_edit.html', context)


@login_required
def service_delete_page(request, hostname):
    if request.method == "POST":

        try:
            this_service = Service.objects.get(hostname=hostname)
            this_account = this_service.account
            this_service.delete()
            Notification.objects.create(account=this_account, description="Service \"%s\" deleted." % (hostname), status="danger")

        except Exception as e:
            context = {
                    "service": Service.objects.get(hostname=hostname),
                    "form_message": {"error": "Service error", "message": str(e), "type": "danger"}
                    }
            return render(request, 'service_delete.html', context)

        return HttpResponseRedirect(reverse('index_page'))

    else:

        context = { "service": Service.objects.get(hostname=hostname) }
        return render(request, 'service_delete.html', context)


def invoice_page(request):
    from django_xhtml2pdf.utils import generate_pdf
    resp = HttpResponse(content_type='application/pdf')
    context = {
            "user": request.user,
            "invoice_number": 124124,
            "services": Service.objects.filter(account=request.user)
            }
    result = generate_pdf('invoice.html', file_object=resp, context=context)
    return result
