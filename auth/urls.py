# core/urls.py
from django.urls import path
from auth import views

urlpatterns = [
    path('signup/', views.register_user, name='signup'),
    # path('verify-email/', views.verify_email, name='verify-email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('send-message/', views.send_message, name='send_message'),
]

