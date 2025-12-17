import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MOVIES_FILE
from utils.helpers import Helper

class MovieRepository:
    # Set up the in-memory movie store and load data
    def __init__(self):
        self.movies = {}
        self.load()
    
    # Load movies from disk or populate with defaults
    def load(self):
        self.movies = Helper.load_json(MOVIES_FILE, self.get_default_movies())
        if not self.movies:
            self.movies = self.get_default_movies()
            self.save()
    
    # Save the current movie dictionary back to disk
    def save(self):
        Helper.save_json(MOVIES_FILE, self.movies)
    
    # Return a built‑in set of movies used as a fallback
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
    
    # Get a single movie by its key
    def get(self, movie_key):
        return self.movies.get(movie_key)
    
    # Return the full movie mapping
    def get_all(self):
        return self.movies
    
    # Search movies by matching a query against several fields
    def search(self, query):
        query_lower = query.lower()
        results = []
        
        for key, movie in self.movies.items():
            # Create searchable text
            searchable = f"{movie['title']} {key} {movie['genre']} {movie['description']} {movie['director']} {' '.join(movie['cast'])}"
            
            if query_lower in searchable.lower():
                results.append((key, movie))
        
        return results
    
    # Add a new movie entry and save
    def add(self, movie_key, movie_data):
        self.movies[movie_key] = movie_data
        self.save()
        return True
    
    # Update an existing movie if it exists
    def update(self, movie_key, updates):
        if movie_key in self.movies:
            self.movies[movie_key].update(updates)
            self.save()
            return True
        return False
    
    # Delete a movie by key if present
    def delete(self, movie_key):
        if movie_key in self.movies:
            del self.movies[movie_key]
            self.save()
            return True
        return False
    
    # Return movies filtered by genre name
    def get_by_genre(self, genre):
        return {k: v for k, v in self.movies.items() if v['genre'].lower() == genre.lower()}
    
    # Return movies filtered by age rating
    def get_by_rating(self, rating):
        return {k: v for k, v in self.movies.items() if v['rating'] == rating}

if __name__ == "__main__":
    pass
    # print("MovieRepository module loaded successfully!")
    
