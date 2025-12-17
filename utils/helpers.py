import json
from datetime import datetime
import random
import sys
import os

class Helper:
    
    # Load JSON from a file path, falling back to a default on error
    @staticmethod
    def load_json(filepath, default=None):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default if default is not None else {}
    
    # Save a Python object as pretty‑printed JSON
    @staticmethod
    def save_json(filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Return a time‑of‑day greeting based on the current hour
    @staticmethod
    def get_greeting():
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"
    
    # Turn a list of (row, number) pairs into a simple string
    @staticmethod
    def format_seat_list(seats):
        return ', '.join([f"{row}{num}" for row, num in seats])
    
    # Format a price with a pound sign and two decimals
    @staticmethod
    def format_price(price):
        return f"£{price:.2f}"
    
    # Format an ISO datetime string into a readable form
    @staticmethod
    def format_datetime(dt_string):
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime('%A, %B %d, %Y at %H:%M')
    
    # Generate a simple random-looking booking reference
    @staticmethod
    def generate_reference():
        return f"BK{random.randint(10000, 99999)}"

if __name__ == "__main__":
    print("Helper module loaded successfully!")