from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import random
import string


def generate_baseservice_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not BaseService.objects.filter(pk=id).exists():
            return 'service-' + id 


def generate_accountservice_id():
    while True:
        id = ''.join(random.sample(string.lowercase + string.digits, 16))
        if not BaseService.objects.filter(pk=id).exists():
            return 'account-' + id 


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.  """
        user = self.create_user(email, password=password,)
        user.is_admin = True
        user.save(using=self._db)
        return user


class BaseService(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=generate_baseservice_id, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    capacity = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'base_services'


class AccountService(models.Model):
    STATE_ACTIVE = 'active' #RUN
    STATE_STANDBY = 'standby'#PAUSE
    STATE_STOPPED = 'stopped'#STOP
    STATE_CHOICES = (
            (STATE_ACTIVE, 'active'),
            (STATE_STANDBY, 'standby'),
            (STATE_STOPPED, 'stopped'),
            )
    id = models.CharField(max_length=24, primary_key=True, default=generate_accountservice_id, editable=False)
    service_type = models.ForeignKey(BaseService)
    ip_address = models.IPAddressField()
    status = models.CharField(max_length=10, choices=STATE_CHOICES, default=STATE_ACTIVE)
    users = models.PositiveIntegerField()

    @property
    def disk_size(self):
        return self.users * BaseService.objects.get(id=self.service_type_id).capacity

    @property
    def current_bill(self):
        import decimal
        return self.users * decimal.Decimal(BaseService.objects.get(id=self.service_type_id).rate)

    def __unicode__(self):
        return self.service_type.name

    class Meta:
        db_table = 'account_services'


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        primary_key=True,
        editable=False,
    )
    services = models.ManyToManyField(AccountService)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True, editable=False)

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
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'accounts'

