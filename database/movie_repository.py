import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MOVIES_FILE
from utils.helpers import Helper

class MovieRepository:
    """
    Repository for movie data operations
    Handles CRUD operations for movies
    """
    
    def __init__(self):
        self.movies = {}
        self.load()
    
    def load(self):
        """Load movies from JSON file"""
        self.movies = Helper.load_json(MOVIES_FILE, self.get_default_movies())
        if not self.movies:
            self.movies = self.get_default_movies()
            self.save()
    
    def save(self):
        """Save movies to JSON file"""
        Helper.save_json(MOVIES_FILE, self.movies)
    
    def get_default_movies(self):
        """Return default movie database"""
        return {
            'joker2': {
                'title': 'Joker: Folie a Deux',
                'genre': 'thriller',
                'rating': '15',
                'duration': '138 mins',
                'description': 'Failed comedian Arthur Fleck meets the love of his life, Harley Quinn, while in Arkham State Hospital.',
                'director': 'Todd Phillips',
                'cast': ['Joaquin Phoenix', 'Lady Gaga'],
                'times': ['14:00', '17:30', '20:00'],
                'price': 12.50,
                'release_year': 2024
            },
            'dune2': {
                'title': 'Dune: Part Two',
                'genre': 'sci-fi',
                'rating': '12A',
                'duration': '166 mins',
                'description': 'Paul Atreides unites with Chani and the Fremen while seeking revenge against those who destroyed his family.',
                'director': 'Denis Villeneuve',
                'cast': ['Timothée Chalamet', 'Zendaya', 'Rebecca Ferguson'],
                'times': ['13:00', '16:30', '19:45'],
                'price': 12.50,
                'release_year': 2024
            },
            'paddington3': {
                'title': 'Paddington in Peru',
                'genre': 'family',
                'rating': 'PG',
                'duration': '106 mins',
                'description': 'Paddington returns to Peru to visit his beloved Aunt Lucy at the Home for Retired Bears.',
                'director': 'Dougal Wilson',
                'cast': ['Ben Whishaw', 'Hugh Bonneville', 'Emily Mortimer'],
                'times': ['11:00', '14:00', '16:30'],
                'price': 10.00,
                'release_year': 2024
            }
        }
    
    def get(self, movie_key):
        """Get a single movie by key"""
        return self.movies.get(movie_key)
    
    def get_all(self):
        """Get all movies"""
        return self.movies
    
    def search(self, query):
        """Search movies by query string"""
        query_lower = query.lower()
        results = []
        
        for key, movie in self.movies.items():
            # Create searchable text
            searchable = f"{movie['title']} {key} {movie['genre']} {movie['description']} {movie['director']} {' '.join(movie['cast'])}"
            
            if query_lower in searchable.lower():
                results.append((key, movie))
        
        return results
    
    def add(self, movie_key, movie_data):
        """Add a new movie"""
        self.movies[movie_key] = movie_data
        self.save()
        return True
    
    def update(self, movie_key, updates):
        """Update an existing movie"""
        if movie_key in self.movies:
            self.movies[movie_key].update(updates)
            self.save()
            return True
        return False
    
    def delete(self, movie_key):
        """Delete a movie"""
        if movie_key in self.movies:
            del self.movies[movie_key]
            self.save()
            return True
        return False
    
    def get_by_genre(self, genre):
        """Get all movies of a specific genre"""
        return {k: v for k, v in self.movies.items() if v['genre'].lower() == genre.lower()}
    
    def get_by_rating(self, rating):
        """Get all movies with a specific rating"""
        return {k: v for k, v in self.movies.items() if v['rating'] == rating}

if __name__ == "__main__":
    pass
    # print("MovieRepository module loaded successfully!")
    
