from django.contrib import admin
from core.models import BaseService, AccountService, Account


admin.site.register(BaseService)
admin.site.register(AccountService)
admin.site.register(Account)

