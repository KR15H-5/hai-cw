import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SEATS_PER_ROW, ROWS, MAX_TICKETS, MIN_TICKETS
from utils.text_processor import TextProcessor
from utils.validators import Validator
from utils.helpers import Helper

class BookingHandler:
    """
    Handles booking flow logic
    Validates each step of the booking process
    """
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.text_processor = TextProcessor()
        self.validator = Validator()
    
    def start(self, movie_key):
        """Start booking for a movie"""
        movie = self.db.get_movie(movie_key)
        if not movie:
            return None, "Sorry, that movie isn't available."
        return movie, None
    
    def validate_time(self, movie, time_input):
        """Validate and match showtime"""
        is_valid, result = self.validator.validate_time(time_input, movie['times'])
        if is_valid:
            return result, None
        return None, f"That time isn't available. Choose from: {', '.join(movie['times'])}"
    
    def validate_tickets(self, num_input):
        """Validate number of tickets"""
        num = self.text_processor.extract_number(num_input)
        
        if num is None:
            return None, "Please enter a valid number of tickets (1-10)."
        
        is_valid, error = self.validator.validate_ticket_count(num)
        if not is_valid:
            return None, error
        
        return num, None
    
    def show_seat_map(self, movie_key, showtime):
        """Generate ASCII seat map"""
        taken = self.db.get_taken_seats(movie_key, showtime)
        
        output = "\n       SCREEN\n\n"
        output += "    " + " ".join([f"{i:2}" for i in range(1, SEATS_PER_ROW + 1)]) + "\n"
        
        for row in ROWS:
            output += f"{row}  "
            for seat_num in range(1, SEATS_PER_ROW + 1):
                if (row, seat_num) in taken:
                    output += " ❌ "
                else:
                    output += " ✅ "
            output += "\n"
        
        output += "\n✅ = Available  ❌ = Taken"
        return output
    
    def validate_seats(self, seat_input, movie_key, showtime, num_tickets):
        """Validate seat selection"""
        seats = self.text_processor.parse_seats(seat_input)
        
        if not seats:
            return None, "Invalid format. Use format like: A1, B5, C3"
        
        taken = self.db.get_taken_seats(movie_key, showtime)
        selected = []
        errors = []
        
        for row, seat_num in seats:
            is_valid, error = self.validator.validate_seat(row, seat_num)
            
            if not is_valid:
                errors.append(f"{row}{seat_num} ({error})")
                continue
            
            if (row, seat_num) in taken:
                errors.append(f"{row}{seat_num} (taken)")
                continue
            
            if (row, seat_num) in selected:
                errors.append(f"{row}{seat_num} (duplicate)")
                continue
            
            selected.append((row, seat_num))
        
        if len(selected) != num_tickets:
            msg = f"Selected {len(selected)} but need {num_tickets}."
            if errors:
                msg += f"\nProblems: {', '.join(errors)}"
            return None, msg
        
        if errors:
            return None, f"Problems: {', '.join(errors)}"
        
        return selected, None
    
    def confirm(self, user_id, user_name, movie_key, time, tickets, seats, total):
        """Confirm and create booking"""
        ref = Helper.generate_reference()
        
        booking_data = {
            'reference': ref,
            'user_id': user_id,
            'user_name': user_name,
            'movie_key': movie_key,
            'movie_title': self.db.get_movie(movie_key)['title'],
            'time': time,
            'tickets': tickets,
            'seats': [[r, n] for r, n in seats],
            'total': total
        }
        
        self.db.add_booking(booking_data)
        
        return ref

if __name__ == "__main__":
    print("✅ BookingHandler module loaded successfully!")