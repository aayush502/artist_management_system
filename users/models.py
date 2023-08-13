from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    # Custom user model manager where email is the unique identifier for authentication instead of username
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('super-admin', 'Super Admin'),
        ('artist-manager', 'Artist Manager'),
        ('artist', 'Artist')
    )
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    )
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3}\s)?\d{10}$', message="Phone number can be entered in the format: '+977 999999999' or '9999999999'. At least 10 digit needed.")
    def validate_past_date(value):
        if value > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[phone_regex])
    dob = models.DateField(validators=[validate_past_date])
    gender = models.CharField(max_length=10, choices=GENDER, default='male')
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLES, default='artist')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'dob']

    def __str__(self):
        return self.email
    
    
