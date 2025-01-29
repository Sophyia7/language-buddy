from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages 
import requests

from chats.chat_service import ChatService

from auth.appwrite_config import database_service, DATABASE_ID, PROFILES_COLLECTION_ID

from appwrite.query import Query
from appwrite.id import ID
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
import os



chat_service = ChatService()    


async def conversation_view(request):
    if not request.session.get('user_id'):
        messages.warning(request, 'Please login to access chat')
        return redirect('login')

    if request.method == 'POST':
        try:
            message = request.POST.get('message', '')

            # Get user profile from Appwrite
            profile = database_service.list_documents(
                DATABASE_ID,
                PROFILES_COLLECTION_ID,
                [Query.equal("user_id", request.session['user_id'])]
            )

            # Get user profile from appwrite
            user_profile = profile['documents'][0]



            # Get AI response using test profile for now
            response = await chat_service.get_response(
                message=message,
                user_profile=user_profile
            )

            # Save converstion to Appwrite
            conversation = database_service.create_document(
                database_id=DATABASE_ID,
                collection_id=os.getenv('CONVERSATION_COLLECTION_ID'),
                document_id=ID.unique(),
                data={
                    'user_id': request.session['user_id'],
                    'conversation_id': ID.unique(),
                    'message': message,
                    'response': response['content'],
                    'created_at': datetime.now().isoformat(),
                    'learning_language': user_profile.get('learning_language'),
                    'message_type': 'user', 
                }
            )

            
            if response and response.get('content'):
                return JsonResponse({
                    'content': response['content']
                })
            else:
                raise Exception("Empty response from AI")
            
        except Exception as e:
            print(f"Chat error: {str(e)}")

            return JsonResponse({
                'error': 'Failed to get response from AI'
            }, status=500)
    
    # GET request - render chat interface
    return render(request, 'chats/conversation.html')  