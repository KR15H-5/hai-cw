import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from config import CONTEXT_FILE
from utils.helpers import Helper

class MemoryStore:
    """
    Persistent storage for user contexts
    Handles saving/loading user data to/from JSON
    """
    
    def __init__(self):
        self.contexts = Helper.load_json(CONTEXT_FILE, {})
    
    def load_context(self, user_id):
        """Load context for a specific user"""
        if user_id not in self.contexts:
            self.contexts[user_id] = self.create_new_context(user_id)
        return self.contexts[user_id]
    
    def save_context(self, user_id, context):
        """Save context for a specific user"""
        self.contexts[user_id] = context
        Helper.save_json(CONTEXT_FILE, self.contexts)
    
    def create_new_context(self, user_id):
        """Create a new empty context for a user"""
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
        """Delete a user's context"""
        if user_id in self.contexts:
            del self.contexts[user_id]
            Helper.save_json(CONTEXT_FILE, self.contexts)
    
    def get_all_contexts(self):
        """Get all stored contexts"""
        return self.contexts

if __name__ == "__main__":
    print("✅ MemoryStore module loaded successfully!")
    
    # Quick test
    store = MemoryStore()
    print(f"\n🧪 Quick Test:")
    print(f"Total stored contexts: {len(store.get_all_contexts())}")