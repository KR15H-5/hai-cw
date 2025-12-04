import json
from datetime import datetime
import random
import sys
import os

class Helper:
    
    @staticmethod
    def load_json(filepath, default=None):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default if default is not None else {}
    
    @staticmethod
    def save_json(filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def get_greeting():
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"
    
    @staticmethod
    def format_seat_list(seats):
        return ', '.join([f"{row}{num}" for row, num in seats])
    
    @staticmethod
    def format_price(price):
        return f"£{price:.2f}"
    
    @staticmethod
    def format_datetime(dt_string):
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime('%A, %B %d, %Y at %H:%M')
    
    @staticmethod
    def generate_reference():
        return f"BK{random.randint(10000, 99999)}"

if __name__ == "__main__":
    print("Helper module loaded successfully!")