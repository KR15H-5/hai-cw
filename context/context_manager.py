import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from .state_tracker import StateTracker
from .memory_store import MemoryStore

class ContextManager:
    """
    Main context manager
    Orchestrates user context, state tracking, and memory storage
    """
    
    def __init__(self, user_id='default_user'):
        self.user_id = user_id
        self.state_tracker = StateTracker()
        self.memory_store = MemoryStore()
        self.context = self.memory_store.load_context(user_id)
    
    def get(self, key, default=None):
        """Get a value from context"""
        return self.context.get(key, default)
    
    def set(self, key, value):
        """Set a value in context"""
        self.context[key] = value
        self.save()
    
    def update(self, updates):
        """Update multiple values in context"""
        self.context.update(updates)
        self.save()
    
    def get_booking_state(self):
        """Get current booking state"""
        return self.state_tracker.get_state(self.context)
    
    def update_booking_state(self, updates):
        """Update booking state"""
        self.state_tracker.update_state(self.context, updates)
        self.save()
    
    def reset_booking(self):
        """Reset booking state"""
        self.state_tracker.reset_state(self.context)
        self.context['awaiting_confirmation'] = False
        self.save()
    
    def add_to_history(self, user_message, bot_response):
        """Add interaction to conversation history"""
        if 'conversation_history' not in self.context:
            self.context['conversation_history'] = []
        
        self.context['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'bot': bot_response
        })
        
        # Keep only last 50 interactions
        if len(self.context['conversation_history']) > 50:
            self.context['conversation_history'] = self.context['conversation_history'][-50:]
        
        self.save()
    
    def save(self):
        """Save context to persistent storage"""
        self.context['last_active'] = datetime.now().isoformat()
        self.memory_store.save_context(self.user_id, self.context)
    
    def clear(self):
        """Clear user context"""
        self.context = self.memory_store.create_new_context(self.user_id)
        self.save()
    
    def get_booking_progress(self):
        """Get booking progress percentage"""
        return self.state_tracker.get_progress(self.context)
    
    def is_in_booking(self):
        """Check if user is in booking flow"""
        return self.state_tracker.is_in_booking(self.context)

if __name__ == "__main__":
    print("ContextManager module loaded successfully!")
    