import google.generativeai as genai 
from django.conf import settings
from datetime import datetime
import os
from dotenv import load_dotenv
from chats.gemini_config import generation_config, safety_settings
import markdown 

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# The service that handles the AI interation with users
class ChatService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        print(GEMINI_API_KEY)

        # Initialize model 
        self.model = genai.GenerativeModel(
          model_name='gemini-pro',
          generation_config=generation_config,
          safety_settings=safety_settings,
        )
        self.chat = None 
        

    async def get_response(self, message, user_profile, chat_history=None):
      try:
        if not self.chat:
          learning_language = user_profile.get('learning_language')
          native_language = user_profile.get('native_language')
          proficiency_level = user_profile.get('proficiency_level')

          # Create context prompt 
          context = f"""
          You are a professional language learning coach. 
          The user is learning {learning_language} and their profiency level is {proficiency_level}, 

          Respond in {learning_language} and provide corrections in {native_language} when they make a mistake.
          Switch to {native_language} if the user is struggling to understand.
          Keep responses natural and conversational. Your goal is ensure the user learns their {learning_language}.
          """

          # Format your responses:
          #   - Use **bold** for words being taught/explained
          #   - Use > for example sentences
          #   - Use --- to separate explanations in {native_language}
          #   - Use bullet points for multiple examples
          #   - Use tables for conjugations if needed

          self.chat = self.model.start_chat(history=[])
          response = self.chat.send_message(context)

        response = self.chat.send_message(message)

        # Convert response to HTML using markdown
        formatted_content = markdown.markdown(
                response.text,
                extensions=['tables', 'fenced_code']
            )

        return {
          'content': formatted_content,
          'timestamp': datetime.now().isoformat(),
        }
      except Exception as e: 
        print(f"Gemini API error: {str(e)}")
        return {
          'content': "I apologize, but I am having trouble responding right now. Give me a minute, please.",
          'timestamp': datetime.now().isoformat(),
        } 