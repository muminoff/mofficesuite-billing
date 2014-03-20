from django.contrib import admin
from core.models import Plan, Service, Account, Invoice


admin.site.register(Plan)
admin.site.register(Service)
admin.site.register(Account)
admin.site.register(Invoice)

