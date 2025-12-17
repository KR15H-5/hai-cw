import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from config import CONTEXT_FILE
from utils.helpers import Helper

# MemoryStore is a class that handles the state of the conversation between the user and the chatbot.
class MemoryStore:
    
    def __init__(self):
        self.contexts = Helper.load_json(CONTEXT_FILE, {})
    
    def load_context(self, user_id):
        if user_id not in self.contexts:
            self.contexts[user_id] = self.create_new_context(user_id)
        return self.contexts[user_id]
    
    def save_context(self, user_id, context):
        self.contexts[user_id] = context
        Helper.save_json(CONTEXT_FILE, self.contexts)
    
    def create_new_context(self, user_id):
        return {
            'user_id': user_id,
            'name': None,
            'preferences': {},
            'conversation_history': [],
            'booking_state': {
                'stage': None,
                'movie': None,
                'time': None,
                'tickets': None,
                'seats': []
            },
            'last_mentioned_movie': None,
            'awaiting_confirmation': False,
            'session_start': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat()
        }
    
    def delete_context(self, user_id):
        if user_id in self.contexts:
            del self.contexts[user_id]
            Helper.save_json(CONTEXT_FILE, self.contexts)
    
    def get_all_contexts(self):
        return self.contexts

if __name__ == "__main__":
    pass
    # print("MemoryStore module loaded successfully!")
    