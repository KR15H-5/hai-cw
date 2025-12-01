import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .movie_repository import MovieRepository
from .booking_repository import BookingRepository

class DatabaseManager:
    """
    Main database manager
    Coordinates all repository operations
    """
    
    def __init__(self):
        self.movie_repo = MovieRepository()
        self.booking_repo = BookingRepository()
        self.initialize()
    
    def initialize(self):
        """Initialize database"""
        self.movie_repo.load()
        self.booking_repo.load()
    
    # Movie operations
    def get_movie(self, movie_key):
        """Get a single movie"""
        return self.movie_repo.get(movie_key)
    
    def get_all_movies(self):
        """Get all movies"""
        return self.movie_repo.get_all()
    
    def search_movies(self, query):
        """Search for movies"""
        return self.movie_repo.search(query)
    
    def add_movie(self, movie_key, movie_data):
        """Add a new movie"""
        return self.movie_repo.add(movie_key, movie_data)
    
    def update_movie(self, movie_key, updates):
        """Update a movie"""
        return self.movie_repo.update(movie_key, updates)
    
    def delete_movie(self, movie_key):
        """Delete a movie"""
        return self.movie_repo.delete(movie_key)
    
    # Booking operations
    def add_booking(self, booking_data):
        """Add a new booking"""
        return self.booking_repo.add(booking_data)
    
    def get_user_bookings(self, user_id):
        """Get all bookings for a user"""
        return self.booking_repo.get_by_user(user_id)
    
    def get_booking_by_reference(self, reference):
        """Get a booking by reference"""
        return self.booking_repo.get_by_reference(reference)
    
    def get_taken_seats(self, movie_key, showtime):
        """Get taken seats for a movie/showtime"""
        return self.booking_repo.get_taken_seats(movie_key, showtime)
    
    def is_seat_taken(self, movie_key, showtime, seat):
        """Check if a specific seat is taken"""
        taken = self.get_taken_seats(movie_key, showtime)
        return seat in taken
    
    def get_all_bookings(self):
        """Get all bookings"""
        return self.booking_repo.get_all()

if __name__ == "__main__":
    print("DatabaseManager module loaded successfully!")
    
    # Quick test
    db = DatabaseManager()
    print(f"\nQuick Test:")
    print(f"Movies: {len(db.get_all_movies())}")
    print(f"Bookings: {len(db.get_all_bookings())}")