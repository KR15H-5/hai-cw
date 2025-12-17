import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SEATS_PER_ROW, ROWS, MAX_TICKETS, MIN_TICKETS
from utils.text_processor import TextProcessor
from utils.validators import Validator
from utils.helpers import Helper

class BookingHandler:
    # Set up helpers for working with bookings and user input
    def __init__(self, db_manager):
        self.db = db_manager
        self.text_processor = TextProcessor()
        self.validator = Validator()
    
    # Start a booking by checking that the movie exists
    def start(self, movie_key):
        movie = self.db.get_movie(movie_key)
        if not movie:
            return None, "Sorry, that movie isn't available."
        return movie, None
    
    # Check whether the requested showtime is valid for the movie
    def validate_time(self, movie, time_input):
        is_valid, result = self.validator.validate_time(time_input, movie['times'])
        if is_valid:
            return result, None
        return None, f"That time isn't available. Choose from: {', '.join(movie['times'])}"
    
    # Validate and normalise the number of tickets requested
    def validate_tickets(self, num_input):
        num = self.text_processor.extract_number(num_input)
        
        if num is None:
            return None, "Please enter a valid number of tickets (1-10)."
        
        is_valid, error = self.validator.validate_ticket_count(num)
        if not is_valid:
            return None, error
        
        return num, None
    
    # Build a simple ASCII seating chart showing taken and free seats
    def show_seat_map(self, movie_key, showtime):
        taken = self.db.get_taken_seats(movie_key, showtime)
        
        output = "\n       SCREEN\n\n"
        output += "    " + " ".join([f"{i:2}" for i in range(1, SEATS_PER_ROW + 1)]) + "\n"
        
        for row in ROWS:
            output += f"{row}  "
            for seat_num in range(1, SEATS_PER_ROW + 1):
                if (row, seat_num) in taken:
                    output += " X "
                else:
                    output += " O "
            output += "\n"
        
        output += "\nO = Available  X = Taken"
        return output
    
    # Validate each selected seat against rules and taken seats
    def validate_seats(self, seat_input, movie_key, showtime, num_tickets):
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
    
    # Create and store a booking record, returning its reference
    def confirm(self, user_id, user_name, movie_key, time, tickets, seats, total):
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
    print("BookingHandler module loaded successfully!")