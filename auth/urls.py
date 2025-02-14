from django.urls import path
from auth import views

urlpatterns = [
    path('signup/', views.register_user, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('update-profile/', views.profile_update_view, name='update_profile'),
]

