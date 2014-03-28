from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from encrypted_fields import EncryptedTextField

import random
import string
from decimal import Decimal

from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
Session._meta.db_table = 'sessions'
Site._meta.db_table = 'sites'
LogEntry._meta.db_table = 'admin_log'
ContentType._meta.db_table = 'content_types'
Permission._meta.db_table = 'moffice_auth_perm'
Group._meta.db_table = 'moffice_auth_group'


def generate_account_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not Account.objects.filter(pk=id).exists():
            return 'account-' + id


def generate_crew_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not Crew.objects.filter(pk=id).exists():
            return 'crew-' + id


def generate_plan_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not Plan.objects.filter(pk=id).exists():
            return 'plan-' + id


def generate_service_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not Service.objects.filter(pk=id).exists():
            return 'service-' + id


def generate_activation_token():
    while True:
        token = ''.join(random.choice(
            string.lowercase +
            string.digits
            ) for x in range(64))
        if not ActivationToken.objects.filter(token=token).exists():
            return token


def generate_reset_token():
    while True:
        token = ''.join(random.choice(
            string.lowercase +
            string.digits) for x in range(64))
        if not ResetToken.objects.filter(token=token).exists():
            return token


def generate_invoice_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not Invoice.objects.filter(pk=id).exists():
            return 'invoice-' + id


def generate_notification_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not Notification.objects.filter(pk=id).exists():
            return 'notification-' + id


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_crew = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    id = models.CharField(max_length=24, primary_key=True, default=generate_account_id, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        editable=False,
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    # first_name = EncryptedTextField()
    # last_name = EncryptedTextField()
    # company_address = EncryptedTextField()
    # company_name = EncryptedTextField()
    # phone_number = EncryptedTextField()
    balance = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    is_activated = models.BooleanField(default=True)
    joined_date = models.DateTimeField(auto_now_add=True, editable=False)
    subscribed_to_news = models.BooleanField(default=True)
    is_crew = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def get_current_state_bill(self):
        amount_sum = 0
        for service in self.services.all():
            amount_sum += service.current_bill

        return amount_sum

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def has_balance(self):
        return self.balance >= Decimal('1.00')

    def __unicode__(self):
        return self.email

    class Meta:
        db_table = 'accounts'
        ordering = ['-joined_date', 'email']


class Plan(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=generate_plan_id, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    capacity = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'plans'
        ordering = ['rate', 'name']


class Service(models.Model):
    STATE_ACTIVE = 'active'
    STATE_STANDBY = 'standby'
    STATE_STOPPED = 'stopped'
    STATE_CHOICES = (
            (STATE_ACTIVE, 'active'),
            (STATE_STANDBY, 'standby'),
            (STATE_STOPPED, 'stopped'),
            )
    id = models.CharField(max_length=24, primary_key=True, default=generate_service_id, editable=False)
    hostname = models.CharField(max_length=255, null=False, blank=False)
    plan = models.ForeignKey(Plan)
    users = models.PositiveIntegerField()
    account = models.ForeignKey(Account)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATE_CHOICES, default=STATE_ACTIVE)

    @property
    def get_status_label(self):
        if self.status == "active": return "success"
        if self.status == "standby": return "warning"
        if self.status == "stopped": return "danger"

    @property
    def disk_size(self):
        return self.users * Plan.objects.get(id=self.plan_id).capacity

    @property
    def calculate_monthly_bill(self):
        import decimal
        monthly_rate = self.users * decimal.Decimal(Plan.objects.get(id=self.plan_id).rate)
        return decimal.Decimal(str("{:.2f}".format(monthly_rate)))

    @property
    def calculate_daily_bill(self):
        import decimal
        import calendar
        import datetime
        now = datetime.datetime.now()
        total_days_in_this_month = calendar.monthrange(now.year, now.month)[1]
        monthly_rate = self.users * decimal.Decimal(Plan.objects.get(id=self.plan_id).rate)
        daily_rate = monthly_rate / total_days_in_this_month
        return decimal.Decimal(str("{:.2f}".format(daily_rate * 12)))

    def __unicode__(self):
        return self.hostname

    class Meta:
        db_table = 'services'


class Invoice(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=generate_invoice_id, editable=False)
    account = models.ForeignKey(Account)
    issued_date = models.DateTimeField(auto_now_add=True, editable=False)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    charged_amount = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    pdf_link = models.URLField()

    def __unicode__(self):
        return '{0} - [{1}]'.format(self.account, self.apply_date.strftime('%m/%d/%Y'))

    class Meta:
        db_table = 'invoices'
        ordering = ['-issued_date']


class Notification(models.Model):
    SUCCESS = 'success'
    WARNING = 'warning'
    INFO = 'info'
    DANGER = 'danger'
    STATE_CHOICES = (
            (SUCCESS, 'success'),
            (WARNING, 'warning'),
            (INFO, 'info'),
            (DANGER, 'danger'),
            )
    id = models.CharField(max_length=32, primary_key=True, default=generate_notification_id, editable=False)
    account = models.ForeignKey(Account)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(null=True, blank=True)
    viewed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATE_CHOICES, default=INFO)

    @property
    def get_status_icon(self):
        if self.status == "success": return "happy"
        if self.status == "warning": return "sad"
        if self.status == "info": return "hourglass"
        if self.status == "danger": return "alarmclock"

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = 'notifications'
        ordering = ['account', '-created_at']


class ActivationToken(models.Model):
    email = models.EmailField(max_length=255, primary_key=True, editable=False)
    token = models.CharField(max_length=64, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.token = generate_activation_token()
        super(ActivationToken, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.token

    class Meta:
        db_table = 'activation_tokens'


class ResetToken(models.Model):
    email = models.EmailField(max_length=255, primary_key=True, editable=False)
    token = models.CharField(max_length=64, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.token = generate_activation_token()
        super(ResetToken, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.token

    class Meta:
        db_table = 'password_reset_tokens'
