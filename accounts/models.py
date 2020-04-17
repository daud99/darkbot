from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    ip_address = models.GenericIPAddressField(default='0.0.0.0')
    number_of_queries = models.PositiveIntegerField(validators=[MaxValueValidator(500)], default=0)
    status = models.CharField(max_length=50, default='Approved')
    request_accepted = models.DateTimeField(default=timezone.now)
    subscription_plan = models.CharField(max_length=8, default='basic')
    company = models.CharField(max_length=255, default='student')
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()




class SubscribeRequest(models.Model):
    ip_address = models.GenericIPAddressField()
    plan_choices = (('Basic','Basic'),('Advance','Advance'),('Pro','Pro'))
    subscription_plan = models.CharField(max_length = 255 ,choices = plan_choices)
    email = models.EmailField()
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    credit_number = models.PositiveIntegerField()
    expiry_month = models.PositiveIntegerField(validators=[MaxValueValidator(12)])
    expiry_year = models.PositiveIntegerField(validators=[MaxValueValidator(9999),])
    security_code = models.PositiveIntegerField()
    status = models.CharField(max_length=50,default='Not Approved')
    created_request = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("index")

class IpWhiteList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ipaddress = models.GenericIPAddressField()

    def __str__(self):
        return self.ipaddress



class IpBlackList(models.Model):
    ipaddress = models.GenericIPAddressField()

    def __str__(self):
        return self.ipaddress

    def get_absolute_url(self):
        return reverse('dashboard:requests')