import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from .state_tracker import StateTracker
from .memory_store import MemoryStore

class ContextManager:

    def __init__(self, user_id='default_user'):
        self.user_id = user_id
        self.state_tracker = StateTracker()
        self.memory_store = MemoryStore()
        self.context = self.memory_store.load_context(user_id)
    
    def get(self, key, default=None):
        return self.context.get(key, default)
    
    def set(self, key, value):
        self.context[key] = value
        self.save()
    
    def update(self, updates):
        self.context.update(updates)
        self.save()
    
    def get_booking_state(self):
        return self.state_tracker.get_state(self.context)
    
    def update_booking_state(self, updates):
        self.state_tracker.update_state(self.context, updates)
        self.save()
    
    def reset_booking(self):
        self.state_tracker.reset_state(self.context)
        self.context['awaiting_confirmation'] = False
        self.save()
    
    def add_to_history(self, user_message, bot_response):
        if 'conversation_history' not in self.context:
            self.context['conversation_history'] = []
        
        self.context['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'bot': bot_response
        })
        
        if len(self.context['conversation_history']) > 50:
            self.context['conversation_history'] = self.context['conversation_history'][-50:]
        
        self.save()
    
    def save(self):
        self.context['last_active'] = datetime.now().isoformat()
        self.memory_store.save_context(self.user_id, self.context)
    
    def clear(self):
        self.context = self.memory_store.create_new_context(self.user_id)
        self.save()
    
    def get_booking_progress(self):
        return self.state_tracker.get_progress(self.context)
    
    def is_in_booking(self):
        return self.state_tracker.is_in_booking(self.context)

if __name__ == "__main__":
    pass
    # print("ContextManager module loaded successfully!")
    