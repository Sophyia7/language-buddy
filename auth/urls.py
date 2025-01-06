from django.urls import path
from auth import views

urlpatterns = [
    path('signup/', views.register_user, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
]

