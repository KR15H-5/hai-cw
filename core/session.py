from datetime import datetime
import random

# Session represents one conversation with a user and tracks its basic stats
class Session:
    
    # Set up a new session for the given user
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_id = self._generate_session_id()
        self.start_time = datetime.now()
        self.last_active = datetime.now()
        self.message_count = 0
    
    # Build a unique session ID using time and a random number
    def _generate_session_id(self):
        timestamp = int(datetime.now().timestamp())
        random_part = random.randint(1000, 9999)
        return f"SESSION_{self.user_id}_{timestamp}_{random_part}"
    
    # Refresh last active time and increment message count
    def update_activity(self):
        self.last_active = datetime.now()
        self.message_count += 1
    
    # Return how long the session has been running in seconds
    def get_duration(self):
        return (datetime.now() - self.start_time).total_seconds()
    
    # Check if the session is still considered active
    def is_active(self):
        inactive_seconds = (datetime.now() - self.last_active).total_seconds()
        return inactive_seconds < 1800  

    # Return a summary of current session statistics
    def get_stats(self):
        return {
            'session_id': self.session_id,
            'duration': self.get_duration(),
            'messages': self.message_count,
            'active': self.is_active()
        }

if __name__ == "__main__":
    pass
    # print("Session module loaded successfully!")
    