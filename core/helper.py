from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

import random
import string
import json


def send_activation_token(request, token):
    variables = Context({
        'request': request,
        'token': token,
    })
    html = get_template('mail/token_html.html').render(variables)
    text = get_template('mail/token_text.html').render(variables)

    msg = EmailMultiAlternatives(
        'Moffice Suite Activation Link',
        text, 'Moffice Suite Billing <billing@mofficesoft.com>',
        [token.email])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass


def send_reset_password(email, password):
    variables = Context({
        'password': password
    })
    html = get_template('mail/password_html.html').render(variables)
    text = get_template('mail/password_text.html').render(variables)

    msg = EmailMultiAlternatives(
        'Moffice Suite Reset Password',
        text, 'Moffice Suite Billing <billing@mofficesoft.com>',
        [email])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass


def generate_random_password(size=8):
    password = ''.join(random.choice(string.lowercase + string.digits + string.uppercase) for x in range(size))
    return password
