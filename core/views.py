from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_page'))

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_page = request.POST.get('next')
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(reverse('account_page'))
            else:
                context = {"form_message": {"error": "Invalid login", "message": "Disabled account"}}
                return render(request, 'login.html', context)

        else:
            context = {"form_message": {"error": "Invalid login", "message": "Incorrect username or password"}}
            return render(request, 'login.html', context)

    else:
        context = {"next": request.GET.get('next')}
        return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))

def signup_page(request):
    return render(request, 'signup.html')

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
