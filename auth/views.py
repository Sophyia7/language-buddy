from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required
import requests
import re

from auth.forms import SignUpForm, LoginForm
from auth.appwrite_config import account_service

from appwrite.exception import AppwriteException
from appwrite.id import ID
import uuid  
                

def register_user(requests):
    if requests.method == 'POST':
        form = SignUpForm(requests.POST)
        if form.is_valid():
            try:
                # Register user with Appwrite
              response = account_service.create(
                  user_id=ID.unique(),
                  email=form.cleaned_data['email'],
                  password=form.cleaned_data['password']
              )

              messages.success(requests, 'Registration successful! Please check your email to verify your account.')
              return redirect('login')
            except AppwriteException as e:
                messages.error(requests, str(e))
    else:
        form = SignUpForm()
    return render(requests, 'auth/signup.html', {'form': form})


# Login view 
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:

                # Retrieve userId from session
                userId = request.session.get('user_id')

                if not userId:
                    messages.error(request, 'User ID not found. Please register again.')
                    # return redirect('register')


                # Sign in user with Appwrite
                session = account_service.create_email_password_session(
                  email=form.cleaned_data['email'],
                  password=form.cleaned_data['password']
                )
                # Store the session in Django's session
                request.session['appwrite_session'] = session
                return redirect('home')
            except AppwriteException as e:
                messages.error(request, str(e))
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})



# Logout
@login_required
def logout_view(request):
    try:
        # Delete the current session
        account.delete_session('current')
        del request.session['appwrite_session']
    except:
        pass
    return redirect('login')

def send_message(request):
    # Your logic here
    return render(request, 'your_template.html')


