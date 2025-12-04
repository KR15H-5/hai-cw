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
        """Validate showtime - accepts multiple formats"""
        # Clean input - remove spaces, fix common typos
        time_clean = time.replace(' ', '').replace(';', ':').lower()
        
        # Handle different input formats
        if ':' not in time_clean:
            if time_clean.isdigit():
                # User entered "11" or "1100"
                if len(time_clean) == 2:  # "11" → "1100"
                    time_clean = time_clean + "00"
                elif len(time_clean) == 3:  # "930" → "0930"
                    time_clean = "0" + time_clean
        
        # Remove colons for comparison
        time_normalized = time_clean.replace(':', '')
        
        # Try to match against available times
        for available in available_times:
            available_normalized = available.replace(':', '').lower()
            
            # Match "1100" against "11:00"
            if time_normalized == available_normalized:
                return True, available
            
            # Also check if user typed exact format
            if time.strip() == available:
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
    print("Validator module loaded successfully!")