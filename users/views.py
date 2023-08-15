from django.shortcuts import render, redirect, get_object_or_404
import requests
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import connection
from .models import User
from django.middleware.csrf import get_token
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                return redirect('user-list')
            messages.success(request, "User created successfully")
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
            return redirect('user-list')
        else:
            error_message = 'Invalid login credentials'
    return render(request, 'users/login.html', {'error_message': error_message})

def logout_user(request):
    logout(request)
    return redirect('login')

def user_list(request):
    response = requests.get(f'http://localhost:8000/api/user-list')
    users = response.json()
    paginator = Paginator(users, per_page=10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'frontend/user-list.html', context={'page': page})

def user_update(request, pk):
    user = User.objects.raw('select * from users_user where id = %s', [pk])
    form = RegistrationForm(instance=user[0])
    if request.method == 'POST':
        url = 'http://localhost:8000/api/user-update/' + str(pk)
        response = requests.patch(url, data=request.POST)
        if response.status_code == 200:
            return redirect('/user-list')        
    return render(request, 'users/register.html', context={'form': form})
