import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .movie_repository import MovieRepository
from .booking_repository import BookingRepository

class DatabaseManager:
    
    
    def __init__(self):
        self.movie_repo = MovieRepository()
        self.booking_repo = BookingRepository()
        self.initialize()
    
    def initialize(self):
        self.movie_repo.load()
        self.booking_repo.load()
    
    
    def get_movie(self, movie_key):
        return self.movie_repo.get(movie_key)
    
    def get_all_movies(self):
        return self.movie_repo.get_all()
    
    def search_movies(self, query):
        return self.movie_repo.search(query)
    
    def add_movie(self, movie_key, movie_data):
        return self.movie_repo.add(movie_key, movie_data)
    
    def update_movie(self, movie_key, updates):
        return self.movie_repo.update(movie_key, updates)
    
    def delete_movie(self, movie_key):
        return self.movie_repo.delete(movie_key)
    
    def add_booking(self, booking_data):
        return self.booking_repo.add(booking_data)
    
    def get_user_bookings(self, user_id):
        return self.booking_repo.get_by_user(user_id)
    
    def get_booking_by_reference(self, reference):
        return self.booking_repo.get_by_reference(reference)
    
    def get_taken_seats(self, movie_key, showtime):
        return self.booking_repo.get_taken_seats(movie_key, showtime)
    
    def is_seat_taken(self, movie_key, showtime, seat):
        taken = self.get_taken_seats(movie_key, showtime)
        return seat in taken
    
    def get_all_bookings(self):
        return self.booking_repo.get_all()

if __name__ == "__main__":
    print("DatabaseManager module loaded successfully!")
    