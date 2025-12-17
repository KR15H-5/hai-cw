import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .movie_repository import MovieRepository
from .booking_repository import BookingRepository

class DatabaseManager:
    
    # Set up the movie and booking repositories and load their data
    def __init__(self):
        self.movie_repo = MovieRepository()
        self.booking_repo = BookingRepository()
        self.initialize()
    
    # Reload data from disk for both repositories
    def initialize(self):
        self.movie_repo.load()
        self.booking_repo.load()
    
    # Get a single movie record by its key
    def get_movie(self, movie_key):
        return self.movie_repo.get(movie_key)
    
    # Return all movies as a dictionary
    def get_all_movies(self):
        return self.movie_repo.get_all()
    
    # Search movies by a free-text query
    def search_movies(self, query):
        return self.movie_repo.search(query)
    
    # Add a new movie to the catalogue
    def add_movie(self, movie_key, movie_data):
        return self.movie_repo.add(movie_key, movie_data)
    
    # Apply updates to an existing movie
    def update_movie(self, movie_key, updates):
        return self.movie_repo.update(movie_key, updates)
    
    # Remove a movie from the catalogue
    def delete_movie(self, movie_key):
        return self.movie_repo.delete(movie_key)
    
    # Add a new booking record via the repository
    def add_booking(self, booking_data):
        return self.booking_repo.add(booking_data)
    
    # Get all bookings made by a specific user
    def get_user_bookings(self, user_id):
        return self.booking_repo.get_by_user(user_id)
    
    # Look up a booking using its reference code
    def get_booking_by_reference(self, reference):
        return self.booking_repo.get_by_reference(reference)
    
    # Get all seats that are already taken for a show
    def get_taken_seats(self, movie_key, showtime):
        return self.booking_repo.get_taken_seats(movie_key, showtime)
    
    def is_seat_taken(self, movie_key, showtime, seat):
        taken = self.get_taken_seats(movie_key, showtime)
        return seat in taken
    
    # Return a list of all bookings
    def get_all_bookings(self):
        return self.booking_repo.get_all()

if __name__ == "__main__":
    print("DatabaseManager module loaded successfully!")
    