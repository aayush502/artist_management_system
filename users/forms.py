from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob', 'address', 'gender', 'password1', 'password2', 'role',]
        widgets = {
            'dob': DateInput(),
            'phone': forms.fields.TextInput(attrs={'placeholder': '+977 9999999999'}),
        }

