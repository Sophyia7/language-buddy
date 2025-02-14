from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.http import urlencode
from django.urls import reverse
from urllib.parse import parse_qs, urlparse
import requests
import re
from datetime import datetime
from dateutil import parser

from auth.forms import SignUpForm, LoginForm, UserProfileForm, ForgotPasswordForm, ResetPasswordForm
from auth.appwrite_config import account_service, database_service, DATABASE_ID, PROFILES_COLLECTION_ID, users_service
# from auth.models import UserProfile


from appwrite.exception import AppwriteException
from appwrite.query import Query
from appwrite.id import ID
import uuid  
import os 

               

def register_user(requests):
    if requests.method == 'POST':
        form = SignUpForm(requests.POST)
        if form.is_valid():
            try:
                # Register user with Appwrite
              response = account_service.create(
                  user_id=ID.unique(),
                  email=form.cleaned_data['email'],
                  password=form.cleaned_data['password'],
                  name=form.cleaned_data['username']
              )

              # Store user data in session for profile setup
              requests.session['user_id'] = response['$id']
              requests.session['email'] = form.cleaned_data['email']
              requests.session['username'] = form.cleaned_data['username']  # Store username

              messages.success(requests, 'Registration successful!')
            #   return redirect('login')
              return redirect('profile_setup')
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
                # Store session data properly
                request.session['jwt'] = session.get('$id')  # Changed from session['jwt']
                request.session['user_id'] = session.get('userId')
                request.session['email'] = form.cleaned_data['email']


                # Check for user's profile
                if not database_service.list_documents(
                    DATABASE_ID,
                    PROFILES_COLLECTION_ID,
                    [
                        Query.equal("user_id", request.session['user_id'])  # Query filter
                    ]
                )['total']:
                    messages.warning(request, 'Please set up your profile!')
                    return redirect('profile_setup')

                # Set cookie session
                response = JsonResponse({"success": True})
                expiry_date_str = session['expire']
                expiry_date = parser.isoparse(expiry_date_str)  
                expiry_timestamp = int(expiry_date.timestamp())
                response.set_cookie(
                    'session',
                    session['secret'],  # Use the session secret as the cookie value
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    expires=expiry_timestamp,
                    path='/'
                )
                
                messages.success(request, 'Login successful!')
                return redirect('chats:chat')

            except AppwriteException as e:
                messages.error(request, str(e))            
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})



# Logout
# @login_required
def logout_view(request):
    try:
        # Get user session data
        user_id = request.session.get('user_id')
        
        if user_id:
            try:
                # Delete Appwrite session
                account_service.delete_session('current')
            except AppwriteException as e:
                print(f"Appwrite session deletion error: {str(e)}")
                
            # Clear Django session regardless of Appwrite status
            request.session.flush()
            messages.success(request, 'Logged out successfully!')
        else:
            messages.warning(request, 'No active session found')
            
    except Exception as e:
        print(f"Logout error: {str(e)}")
        messages.error(request, 'Error during logout')
    
    return redirect('login')



# Profile SetUp view

def profile_setup_view(request):
    if not request.session.get('user_id'):
        return redirect('signup')

    # Check if user already has a profile
    try:
        existing_profile = database_service.list_documents(
            DATABASE_ID,
            PROFILES_COLLECTION_ID,
            [
                Query.equal("user_id", request.session['user_id'])  # Query filter
            ]
        )
        print(existing_profile)

        if existing_profile['total'] > 0:
            messages.warning(request, 'You already have a profile!')
            return redirect('home')
            
    except Exception as e:
        print(f"Error checking existing profile: {str(e)}")
        
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                user_id = str(request.session['user_id']) 
                learning_language = str(form.cleaned_data['learning_language'])

                # Create document directly in view
                result = database_service.create_document(
                    database_id=DATABASE_ID,
                    collection_id=PROFILES_COLLECTION_ID,
                    document_id=ID.unique(),
                    data={
                        # 'user_id': user_id,
                        'user_id': request.session['user_id'],
                        'email': request.session['email'],
                        'username': request.session.get('username', ''),
                        'native_language': form.cleaned_data['native_language'],
                        'learning_language': form.cleaned_data['learning_language'],
                        'proficiency_level': form.cleaned_data['proficiency_level'],
                        'created_at': datetime.now().isoformat()
                    }
                )
  

                # print(f"Session data: {session_data}")
                # print(f"Profile created: {result}")  # Debug logging
                messages.success(request, 'Profile created successfully!')
                return redirect('chats:chat')

            except Exception as e:
                print(f"Error creating profile: {str(e)}")  # Debug logging
                messages.error(request, str(e))
    else:
        form = UserProfileForm()
    
    return render(request, 'auth/profile_setup.html', {'form': form})

def profile_update_view(request):
    try:
        # Get user's current profile
        profile = database_service.list_documents(
            DATABASE_ID,
            PROFILES_COLLECTION_ID,
            [Query.equal("user_id", request.session['user_id'])]
        )['documents'][0]
        
        if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                try:
                    # Update profile in Appwrite
                    database_service.update_document(
                        DATABASE_ID,
                        PROFILES_COLLECTION_ID,
                        profile['$id'],
                        {
                            'native_language': form.cleaned_data['native_language'],
                            'learning_language': form.cleaned_data['learning_language'],
                            'proficiency_level': form.cleaned_data['proficiency_level'],
                        }
                    )
                    messages.success(request, 'Profile updated successfully!')
                    return render(request, 'auth/profile_update.html', {
                        'form': form,
                    })
                except Exception as e:
                    messages.error(request, str(e))
        else:
            # Pre-fill form with current profile data
            form = UserProfileForm(initial={
                'native_language': profile['native_language'],
                'learning_language': profile['learning_language'],
                'proficiency_level': profile['proficiency_level'],
            })
        
        return render(request, 'auth/profile_update.html', {'form': form})
    except Exception as e:
        messages.error(request, 'Error loading profile')
        return redirect('profile_setup')


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                app_url = os.getenv('APP_URL')
                recovery_url = f'{app_url}/auth/reset-password/'
                account_service.create_recovery(
                    email=form.cleaned_data['email'],
                    url=recovery_url
                )
                messages.success(request, 'If the email exists, a reset link will be sent.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Unable to process request.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'auth/forgot_password.html', {'form': form})


def reset_password_view(request):
    user_id = request.GET.get('userId')
    secret = request.GET.get('secret')
    expire = request.GET.get('expire')

    if not user_id or not secret or not expire:
        messages.error(request, 'Invalid reset link.')
        return redirect('forgot_password')


    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'auth/reset_password.html', {'form': form})

            try:
                # Update the user's password
                users_service.update_password(user_id, password)
                messages.success(request, 'Password has been reset successfully!')
                return redirect('login')
            except Exception as e:
                messages.error(request, str(e))
    
    else:
        form = ResetPasswordForm()
    return render(request, 'auth/reset_password.html', {'form': form})