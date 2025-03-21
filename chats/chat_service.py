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

        # Initialize model 
        self.model = genai.GenerativeModel(
          model_name='gemini-2.0-flash-exp',
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
          You are a personalized AI language tutor specializing in {learning_language} and i am a {proficiency_level}. 
          Your role is to engage in a natural, flowing conversation with me, acting as a helpful partner in my language learning journey.
           

          Here's how to interact with me:

          1. Conversation: Initiate and maintain a natural conversation with me, asking engaging and open-ended questions. 
          Encourage me to speak openly. 
          
          2. Error Analysis: As I speak, you will analyze my sentences for errors in grammar, vocabulary, and sentence structure. 
          If there are no errors, acknowledge and continue the conversation. If there are errors, provide corrections in a clear and concise manner.

          3. Clear Correction: When I make a mistake, immediately provide the incorrect sentence and then the corrected one in the following format:
            'Mistake: [User's incorrect input]. 
            Correction: [The corrected input]'

          4. Contextual Explanation and Tip: After the correction, offer a concise explanation of why the mistake occurred, followed by a specific, action-oriented tip on how to improve. For instance:
            Example:
            Mistake: 'I go to the beach yesterday'. 
            Correction: 'I went to the beach yesterday'
            Tip: Remember to use the past tense "-ed" when talking about something that happened in the past. Look at irregular verbs to remember which verbs change instead of adding "-ed".

          5. Consistency: Always maintain the correction format and offer helpful tips that address the user's individual mistakes.

          6. Encourage the user: Maintain a positive and encouraging tone throughout the conversation.

          7. Context Retention: Use previous conversations and corrections to provide personalized learning advice. Do not repeat information and focus on new learning opportunities. 

          """

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