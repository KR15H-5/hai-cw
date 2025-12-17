import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from config import BOOKINGS_FILE
from utils.helpers import Helper

class BookingRepository:
    
    # Create a new booking repository and load existing bookings
    def __init__(self):
        self.bookings = []
        self.taken_seats_cache = {}
        self.load()
    
    # Load bookings from disk and rebuild the taken seats cache
    def load(self):
        self.bookings = Helper.load_json(BOOKINGS_FILE, [])
        self._rebuild_taken_seats_cache()
    
    # Save the current list of bookings back to disk
    def save(self):
        Helper.save_json(BOOKINGS_FILE, self.bookings)
    
    # Rebuild the in-memory map of taken seats for each movie and showtime
    def _rebuild_taken_seats_cache(self):
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
    
    # Add a new booking and update the cache, returning its ID
    def add(self, booking_data):
        booking_data['booking_id'] = len(self.bookings) + 1
        booking_data['timestamp'] = datetime.now().isoformat()
        
        self.bookings.append(booking_data)
        self.save()
        
        movie_key = booking_data['movie_key']
        showtime = booking_data['time']
        seats = [tuple(s) for s in booking_data['seats']]
        
        if movie_key not in self.taken_seats_cache:
            self.taken_seats_cache[movie_key] = {}
        if showtime not in self.taken_seats_cache[movie_key]:
            self.taken_seats_cache[movie_key][showtime] = []
        
        self.taken_seats_cache[movie_key][showtime].extend(seats)
        
        return booking_data['booking_id']
    
    # Return all bookings for a specific user
    def get_by_user(self, user_id):
        return [b for b in self.bookings if b.get('user_id') == user_id]
    
    # Find a single booking by its reference code
    def get_by_reference(self, reference):
        for booking in self.bookings:
            if booking.get('reference') == reference:
                return booking
        return None
    
    # Get a list of seats already taken for a movie and showtime
    def get_taken_seats(self, movie_key, showtime):
        return self.taken_seats_cache.get(movie_key, {}).get(showtime, [])
    
    # Return all stored bookings
    def get_all(self):
        return self.bookings
    
    # Get bookings filtered by movie key
    def get_by_movie(self, movie_key):
        return [b for b in self.bookings if b['movie_key'] == movie_key]
    
    # Get bookings created on a specific date
    def get_by_date(self, date_str):
        return [b for b in self.bookings if b['timestamp'].startswith(date_str)]

if __name__ == "__main__":
    print("BookingRepository module loaded successfully!")
    
