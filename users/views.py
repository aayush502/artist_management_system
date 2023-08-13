from django.shortcuts import render, redirect
from django.views import View
from .models import User
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid login credentials'
    return render(request, 'users/login.html', {'error_message': error_message})

def logout_user(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    return render(request, 'users/dashboard.html', context={})