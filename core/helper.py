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


def send_reset_token(request, token):
    variables = Context({
        'request': request,
        'token': token,
    })
    html = get_template('mail/reset_html.html').render(variables)
    text = get_template('mail/reset_text.html').render(variables)

    msg = EmailMultiAlternatives(
        'Moffice Suite Reset Password Link',
        text, 'Moffice Suite Billing <billing@mofficesoft.com>',
        [token.email])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass


def send_welcome_message(email):
    variables = Context({
        'email': email
    })
    html = get_template('mail/welcome_html.html').render(variables)
    text = get_template('mail/welcome_text.html').render(variables)

    msg = EmailMultiAlternatives(
        'Welcome to Moffice Suite',
        text, 'Moffice Suite <billing@mofficesoft.com>',
        [email])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass


def send_feedback(customer, subject, feedback):
    variables = Context({
        'subject': subject,
        'feedback': feedback,
        'customer': customer
    })
    html = get_template('mail/feedback_html.html').render(variables)
    text = get_template('mail/feedback_text.html').render(variables)

    msg = EmailMultiAlternatives(
        'Feedback from Moffice Suite Customer',
        text, 'Moffice Suite <billing@mofficesoft.com>',
        ['support@mofficesuite.com', 'support@mofficesoft.com', 'sardor@hanbiro.com'])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass


def generate_random_password(size=8):
    password = ''.join(random.choice(string.lowercase + string.digits + string.uppercase) for x in range(size))
    return password


def generate_current_month_invoice(account):
    from django_xhtml2pdf.utils import generate_pdf
    from core.models import Invoice
    context = {
            "user": account,
            "invoice_number": 124124,
            "services": Service.objects.filter(account=request.user)
            }
    result = generate_pdf('invoice.html', file_object=resp, context=context)
    return result
