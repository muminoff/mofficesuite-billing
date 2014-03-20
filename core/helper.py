from django.http import HttpResponse
from django.utils import simplejson as json
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives


def sendEmailToken(request, token):
    variables = Context({
        'request': request,
        'token': token,
    })
    html = get_template('mail/token_html.html').render(variables)
    text = get_template('mail/token_text.html').render(variables)

    msg = EmailMultiAlternatives(
        'Moffice Suite activation link',
        text, 'Moffice Suite Billing <billing@mofficesoft.com>',
        [token.email])
    msg.attach_alternative(html, "text/html")

    try:
        msg.send(fail_silently=True)
    except:
        pass


def render_json(data_dict):
    return HttpResponse(json.dumps(data_dict), 'application/javascript')


def render_template_json(template, context):
    return HttpResponse(render_to_string(template, context), 'application/javascript')
