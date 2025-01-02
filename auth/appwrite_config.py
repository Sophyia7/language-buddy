from appwrite.client import Client 
from appwrite.services.account import Account
from appwrite.services.users import Users 
from appwrite.services.databases import Databases
from appwrite.id import ID
import os 
from dotenv import load_dotenv

load_dotenv()

# Init the Appwrite Client
client = Client()
client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
# client.set_endpoint(os.getenv('http://localhost/v1')) # For local testing
client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
client.set_key(os.getenv('APPWRITE_API_KEY'))

# Init appwrite service
account_service = Account(client)
users_service = Users(client)
database_service = Databases(client)

# Database Configuration
DATABASE_ID = os.getenv('APPWRITE_DATABASE_ID')
PROFILES_COLLECTION_ID = os.getenv('APPWRITE_PROFILES_COLLECTION_ID')

# Database helper functions
# def create_user_profile(session_data, profile_data):
#     try:
#         # Create document and store result
#         result = database_service.create_document(
#             database_id=DATABASE_ID,
#             collection_id=PROFILES_COLLECTION_ID,
#             document_id=ID.unique(),
#             data={
#                 'user_id': session_data['userId'],
#                 'email': session_data['email'],
#                 'username': session_data.get('username', ''),
#                 'native_language': profile_data['native_language'],
#                 'learning_language': profile_data['learning_language'],
#                 'proficiency_level': profile_data['proficiency_level'],
#                 'created_at': datetime.now().isoformat()
#             }
#         )
#         print(f"Profile created: {result}")  # Debug logging
#         return result
        
#     except Exception as e:
#         print(f"Error creating profile: {str(e)}")  # Debug logging
#         raise e
  
def get_user_profile(user_id):
    try:
        return database_service.list_documents(
            database_id=DATABASE_ID,
            collection_id=PROFILES_COLLECTION_ID,
            queries=[f'user_id={user_id}']
        )
    except Exception as e:
        raise Exception(f"Error fetching profile: {str(e)}")