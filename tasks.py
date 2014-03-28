import os
from socket import gethostname

environment = 'production' if gethostname() == 'gwmanage.hanbiro.com' else 'local'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billing.settings." + environment)

from django.http import HttpResponseRedirect, HttpResponse
from django_xhtml2pdf.utils import generate_pdf
from core.models import Account, Service
from celery import Celery

app = Celery('tasks', broker='redis://:gksqlfhWkd!!@localhost:6379/0')


@app.task
def add(x, y):
    return x + y


@app.task
def make_current_month_invoice(email):
    resp = HttpResponse(content_type='application/pdf')
    this_account = Account.objects.get(email=email)
    context = {
            "email": email,
            "invoice_number": 124124,
            "services": Service.objects.filter(account=this_account)
            }
    print generate_pdf('invoice.html', context=context)
