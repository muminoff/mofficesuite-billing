from django.shortcuts import render


def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request, 'signup.html')

def services_page(request):
    return render(request, 'services.html')
