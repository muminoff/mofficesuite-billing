from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def index_page(request):
    return HttpResponseRedirect(reverse('services_page'))

def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request, 'signup.html')

def services_page(request):
    return render(request, 'services.html')

def account_page(request):
    return render(request, 'account.html')

def billing_page(request):
    return render(request, 'billing.html')

def support_page(request):
    return render(request, 'support.html')

def feedback_page(request):
    return render(request, 'feedback.html')

def payment_page(request):
    return render(request, 'payment.html')
