from appwrite.client import Client 
from appwrite.services.account import Account
from appwrite.services.users import Users 
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