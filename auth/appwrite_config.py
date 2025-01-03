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
  
def get_user_profile(user_id):
    try:
        return database_service.list_documents(
            database_id=DATABASE_ID,
            collection_id=PROFILES_COLLECTION_ID,
            queries=[f'user_id={user_id}']
        )
    except Exception as e:
        raise Exception(f"Error fetching profile: {str(e)}")