# /profile_manager.py

from database import DatabaseManager
import json

class ProfileManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_profiles = {
            'chatbot': {'name': 'Default', 'data': {}},
            'user': {'name': 'Guest', 'data': {}}
        }
        self.current_session = None

    def get_profile_options(self, entity_type):
        profiles = self.db.get_profiles(entity_type)
        return ['New Profile'] + list(profiles.keys())

    def load_profile(self, entity_type, profile_name):
        if profile_name == 'New Profile':
            return {'name': '', 'data': {}}
        
        profiles = self.db.get_profiles(entity_type)
        profile_data = profiles.get(profile_name, {})
        
        return {
            'name': profile_name,
            'data': profile_data
        }

    def save_profile(self, entity_type, profile_name, data):
        if not profile_name:
            raise ValueError("Profile name cannot be empty")
        
        self.db.save_profile(entity_type, profile_name, data)
        
        if self.current_profiles[entity_type]['name'] == profile_name:
            self.current_profiles[entity_type]['data'] = data

    def delete_profile(self, entity_type, profile_name):
        if profile_name == 'Default' or profile_name == 'Guest':
            raise ValueError("Cannot delete default profiles")
        
        self.db.delete_profile(entity_type, profile_name)
        
        if self.current_profiles[entity_type]['name'] == profile_name:
            self.reset_profile(entity_type)

    def reset_profile(self, entity_type):
        default_name = 'Default' if entity_type == 'chatbot' else 'Guest'
        self.current_profiles[entity_type] = {
            'name': default_name,
            'data': {}
        }

    def save_chat_session(self, session_name, messages):
        if not session_name:
            raise ValueError("Session name cannot be empty")
        
        self.db.save_chat_session(
            session_name,
            self.current_profiles['chatbot']['name'],
            self.current_profiles['user']['name'],
            messages
        )
        self.current_session = session_name

    def load_chat_sessions(self):
        return self.db.load_chat_sessions()

    def load_chat_history(self, session_id):
        messages = self.db.load_chat_messages(session_id)
        session_info = next(
            (s for s in self.db.load_chat_sessions() if s[0] == session_id),
            None
        )
        
        if session_info:
            self.current_profiles['chatbot']['name'] = session_info[2]
            self.current_profiles['user']['name'] = session_info[3]
            
            chatbot_profile = self.db.get_profiles('chatbot').get(session_info[2], {})
            user_profile = self.db.get_profiles('user').get(session_info[3], {})
            
            self.current_profiles['chatbot']['data'] = chatbot_profile
            self.current_profiles['user']['data'] = user_profile
        
        return messages

    def get_current_profiles(self):
        return self.current_profiles.copy()

    def set_current_profile(self, entity_type, profile_name, data):
        if entity_type not in ['chatbot', 'user']:
            raise ValueError("Invalid entity type")
        
        self.current_profiles[entity_type] = {
            'name': profile_name,
            'data': data
        }

