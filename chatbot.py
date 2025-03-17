# /chatbot.py

from model_loader import ModelLoader
from profile_manager import ProfileManager
import json
import gc

class AIChatbot:
    def __init__(self, profile_manager: ProfileManager):
        self.pm = profile_manager
        self.model_loader = ModelLoader()
        self.chat_history = []
        
        # Default system prompt template
        self.system_template = """[System Context]
{chatbot_profile}

[User Context]
{user_profile}

[Conversation History]
{history}

[Current Interaction]
User : {user_input}
Chatbot: """
        self.load_model()

    def load_model(self):
        self.model = self.model_loader.load_model()
        if not self.model:
            raise RuntimeError("Model not loaded. Please check the model path.")

    def build_prompt(self, user_input):
        chatbot_profile = self.pm.get_current_profiles()['chatbot']
        user_profile = self.pm.get_current_profiles()['user']
        history = "\n".join(self.chat_history)

        return self.system_template.format(
            chatbot_profile=json.dumps(chatbot_profile['data']),
            user_profile=json.dumps(user_profile['data']),
            history=history,
            user_input=user_input
        )

    def respond(self, user_input):
        if not self.model:
            raise RuntimeError("No model loaded to generate a response.")
        
        prompt = self.build_prompt(user_input)
        response = self.model.generate_response(prompt)
        self.chat_history.append(f":User  {user_input}")
        self.chat_history.append(f"Chatbot: {response}")
        
        return response

    def save_chat_history(self, session_name):
        self.pm.save_chat_session(session_name, self.chat_history)

    def load_chat_history(self, session_id):
        self.chat_history = self.pm.load_chat_history(session_id)

    def reset_chat(self):
        self.chat_history = []

    def get_chat_history(self):
        return self.chat_history.copy()

