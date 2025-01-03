from django.urls import path
from chats import views

app_name = 'chats'

urlpatterns = [
   path('new/', views.conversation_view, name='chat')
]
