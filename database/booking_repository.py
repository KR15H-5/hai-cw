import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from config import BOOKINGS_FILE
from utils.helpers import Helper

class BookingRepository:
    """
    Repository for booking data operations
    Handles CRUD operations for bookings
    """
    
    def __init__(self):
        self.bookings = []
        self.taken_seats_cache = {}
        self.load()
    
    def load(self):
        """Load bookings from JSON file"""
        self.bookings = Helper.load_json(BOOKINGS_FILE, [])
        self._rebuild_taken_seats_cache()
    
    def save(self):
        """Save bookings to JSON file"""
        Helper.save_json(BOOKINGS_FILE, self.bookings)
    
    def _rebuild_taken_seats_cache(self):
        """Rebuild the taken seats cache from bookings"""
        self.taken_seats_cache = {}
        for booking in self.bookings:
            movie_key = booking['movie_key']
            showtime = booking['time']
            seats = [tuple(s) for s in booking['seats']]
            
            if movie_key not in self.taken_seats_cache:
                self.taken_seats_cache[movie_key] = {}
            if showtime not in self.taken_seats_cache[movie_key]:
                self.taken_seats_cache[movie_key][showtime] = []
            
            self.taken_seats_cache[movie_key][showtime].extend(seats)
    
    def add(self, booking_data):
        """Add a new booking"""
        booking_data['booking_id'] = len(self.bookings) + 1
        booking_data['timestamp'] = datetime.now().isoformat()
        
        self.bookings.append(booking_data)
        self.save()
        
        # Update taken seats cache
        movie_key = booking_data['movie_key']
        showtime = booking_data['time']
        seats = [tuple(s) for s in booking_data['seats']]
        
        if movie_key not in self.taken_seats_cache:
            self.taken_seats_cache[movie_key] = {}
        if showtime not in self.taken_seats_cache[movie_key]:
            self.taken_seats_cache[movie_key][showtime] = []
        
        self.taken_seats_cache[movie_key][showtime].extend(seats)
        
        return booking_data['booking_id']
    
    def get_by_user(self, user_id):
        """Get all bookings for a specific user"""
        return [b for b in self.bookings if b.get('user_id') == user_id]
    
    def get_by_reference(self, reference):
        """Get a booking by reference number"""
        for booking in self.bookings:
            if booking.get('reference') == reference:
                return booking
        return None
    
    def get_taken_seats(self, movie_key, showtime):
        """Get all taken seats for a movie/showtime"""
        return self.taken_seats_cache.get(movie_key, {}).get(showtime, [])
    
    def get_all(self):
        """Get all bookings"""
        return self.bookings
    
    def get_by_movie(self, movie_key):
        """Get all bookings for a specific movie"""
        return [b for b in self.bookings if b['movie_key'] == movie_key]
    
    def get_by_date(self, date_str):
        """Get all bookings for a specific date"""
        return [b for b in self.bookings if b['timestamp'].startswith(date_str)]

if __name__ == "__main__":
    print("BookingRepository module loaded successfully!")
    
    # Quick test
    repo = BookingRepository()
    print(f"\n🧪 Quick Test:")
    print(f"Total bookings: {len(repo.get_all())}")