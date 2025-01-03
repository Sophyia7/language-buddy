from django.shortcuts import render
from django.http import JsonResponse
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
# CONVERSATION_COLLECTION_ID=os.getenv('CONVERSATION_COLLECTION_ID')


async def conversation_view(request):
    if not request.session.get('user_id'):
        return redirect('login')

    if request.method == 'POST':
        try:
            message = request.POST.get('message', '')
            # learning_language = user_profile.get('learning_language')
            # native_language = user_profile.get('native_language')

            # Get user profile from Appwrite
            profile = database_service.list_documents(
                DATABASE_ID,
                PROFILES_COLLECTION_ID,
                [Query.equal("user_id", request.session['user_id'])]
            )
            
            # Use test profile if none found
            user_profile = profile['documents'][0] if profile['documents'] else {
                'learning_language': 'Spanish',
                'native_language': 'English'
            }


            # Get AI response using test profile for now
            response = await chat_service.get_response(
                message=message,
                user_profile=user_profile
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







# async def chat_message(request):
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         user_id = requests.session.get('user_id')

#         # Get user profile from Appwrite
#         profile = database_service.list_documents(
#             DATABASE_ID,
#             PROFILES_COLLECTION_ID,
#             [
#                 Query.equal("user_id", user_id)
#             ]
#         )

#         # Get chat response 
#         response = await chat_service.get_response(
#             message=message,
#             user_profile=profile['documents'][0]
#         )

#         # Store the conversation in Appwrite 
#         database_service.create_document(
#             DATABASE_ID,
#             MESSAGES_COLLECTION_ID,
#             data={
#                 'user_id': user_id,
#                 'content': message,
#                 'response': response['content'],
#                 'timestamp': response['timestamp']
#             }
#         )

#         return JsonResponse(response)

#     return JsonResponse({'error': 'Invalid request'}, status=400)