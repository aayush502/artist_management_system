from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    # Custom user model manager where email is the unique identifier for authentication instead of username
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
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

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=10, choices=GENDER)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'dob']

    def __str__(self):
        return self.email
