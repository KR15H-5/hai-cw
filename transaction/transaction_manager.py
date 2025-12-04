import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .booking_handler import BookingHandler
from .payment_processor import PaymentProcessor

class TransactionManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.booking_handler = BookingHandler(db_manager)
        self.payment_processor = PaymentProcessor()
    
    def start_booking(self, movie_key):
        return self.booking_handler.start(movie_key)
    
    def validate_time(self, movie, time_input):
        return self.booking_handler.validate_time(movie, time_input)
    
    def validate_tickets(self, num_input):
        return self.booking_handler.validate_tickets(num_input)
    
    def show_seat_map(self, movie_key, showtime):
        return self.booking_handler.show_seat_map(movie_key, showtime)
    
    def validate_seats(self, seat_input, movie_key, showtime, num_tickets):
        return self.booking_handler.validate_seats(seat_input, movie_key, showtime, num_tickets)
    
    def calculate_total(self, movie, num_tickets):
        return self.payment_processor.calculate_total(movie, num_tickets)
    
    def confirm_booking(self, user_id, user_name, movie_key, time, tickets, seats, total):
        return self.booking_handler.confirm(user_id, user_name, movie_key, time, tickets, seats, total)
    
    def process_payment(self, amount, payment_method='card'):
        return self.payment_processor.process(amount, payment_method)

if __name__ == "__main__":
    print("TransactionManager module loaded successfully!")