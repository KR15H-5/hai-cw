from datetime import datetime
import random

class Session:
    """
    Manages user session
    Tracks session duration, activity, and statistics
    """
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_id = self._generate_session_id()
        self.start_time = datetime.now()
        self.last_active = datetime.now()
        self.message_count = 0
    
    def _generate_session_id(self):
        """Generate unique session ID"""
        timestamp = int(datetime.now().timestamp())
        random_part = random.randint(1000, 9999)
        return f"SESSION_{self.user_id}_{timestamp}_{random_part}"
    
    def update_activity(self):
        """Update last active time and increment message count"""
        self.last_active = datetime.now()
        self.message_count += 1
    
    def get_duration(self):
        """Get session duration in seconds"""
        return (datetime.now() - self.start_time).total_seconds()
    
    def is_active(self):
        """Check if session is still active (last activity < 30 min)"""
        inactive_seconds = (datetime.now() - self.last_active).total_seconds()
        return inactive_seconds < 1800  # 30 minutes
    
    def get_stats(self):
        """Get session statistics"""
        return {
            'session_id': self.session_id,
            'duration': self.get_duration(),
            'messages': self.message_count,
            'active': self.is_active()
        }

if __name__ == "__main__":
    pass
    # print("Session module loaded successfully!")
    