import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from config import CONTEXT_FILE
from utils.helpers import Helper

# MemoryStore loads and saves conversation contexts for all users
class MemoryStore:
    
    # Load all contexts from disk when the store is created
    def __init__(self):
        self.contexts = Helper.load_json(CONTEXT_FILE, {})
    
    # Return a context for a user, creating a new one if missing
    def load_context(self, user_id):
        if user_id not in self.contexts:
            self.contexts[user_id] = self.create_new_context(user_id)
        return self.contexts[user_id]
    
    # Persist a single user's context to disk
    def save_context(self, user_id, context):
        self.contexts[user_id] = context
        Helper.save_json(CONTEXT_FILE, self.contexts)
    
    # Create a brand new default context structure for a user
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
    
    # Remove a user's context completely
    def delete_context(self, user_id):
        if user_id in self.contexts:
            del self.contexts[user_id]
            Helper.save_json(CONTEXT_FILE, self.contexts)
    
    # Return the full mapping of user IDs to contexts
    def get_all_contexts(self):
        return self.contexts

if __name__ == "__main__":
    pass
    # print("MemoryStore module loaded successfully!")
    