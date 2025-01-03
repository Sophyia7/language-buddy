from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required
import requests
import re
from datetime import datetime

from auth.forms import SignUpForm, LoginForm, UserProfileForm
from auth.appwrite_config import account_service, database_service, DATABASE_ID, PROFILES_COLLECTION_ID
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
              request.session['username'] = form.cleaned_data['username']  # Store username

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


def home_view(request):
    # template_name = 'core/home.html'
    template_name = 'chats/conversation.html'
    return render(request, template_name)


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
  

                print(f"Session data: {session_data}")
                print(f"Profile created: {result}")  # Debug logging
                messages.success(request, 'Profile created successfully!')
                return redirect('home')

            except Exception as e:
                print(f"Error creating profile: {str(e)}")  # Debug logging
                messages.error(request, str(e))
    else:
        form = UserProfileForm()
    
    return render(request, 'auth/profile_setup.html', {'form': form})