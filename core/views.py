from django.shortcuts import render


def signup_page(request):
    return render(request, 'signup.html')

def login_page(request):
    return render(request, 'login.html')
