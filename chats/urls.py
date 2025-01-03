from django.urls import path
from chats import views

urlpatterns = [
   path('new/', views.conversation_view, name='new chat')
]
