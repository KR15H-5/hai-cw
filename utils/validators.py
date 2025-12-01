import re
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ROWS, SEATS_PER_ROW, MIN_TICKETS, MAX_TICKETS

class Validator:
    
    @staticmethod
    def validate_seat(row, seat_num):
        """Validate seat row and number"""
        if row not in ROWS:
            return False, f"Row must be {ROWS[0]}-{ROWS[-1]}"
        
        if seat_num < 1 or seat_num > SEATS_PER_ROW:
            return False, f"Seat must be 1-{SEATS_PER_ROW}"
        
        return True, None
    
    @staticmethod
    def validate_ticket_count(num):
        """Validate ticket count"""
        if num < MIN_TICKETS:
            return False, f"Minimum {MIN_TICKETS} ticket"
        
        if num > MAX_TICKETS:
            return False, f"Maximum {MAX_TICKETS} tickets"
        
        return True, None
    
    @staticmethod
    def validate_time(time, available_times):
        """Validate showtime"""
        time_clean = time.replace(' ', '').replace(':', '')
        
        for available in available_times:
            available_clean = available.replace(':', '')
            if time_clean == available_clean or time == available:
                return True, available
        
        return False, None
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone):
        """Validate UK phone number"""
        pattern = r'^(\+44|0)[0-9]{10}$'
        return bool(re.match(pattern, phone.replace(' ', '')))

if __name__ == "__main__":
    print("✅ Validator module loaded successfully!")