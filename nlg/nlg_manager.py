import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from .response_generator import ResponseGenerator
from utils.helpers import Helper

class NLGManager:
    """
    Main NLG orchestrator
    Generates all bot responses using templates and dynamic content
    """
    
    def __init__(self):
        self.generator = ResponseGenerator()
    
    def welcome_message(self, name=None):
        """Generate welcome message"""
        greeting = Helper.get_greeting()
        welcome = self.generator.welcome(greeting)
        
        if name:
            greet_user = self.generator.greet_user(name)
            how_help = self.generator.how_can_help()
            return f"{welcome}\n{greet_user} {how_help}\n\nYou can:\n- Ask about movies\n- Book tickets\n- Type 'help' for more options"
        else:
            ask_name = self.generator.ask_name()
            return f"{welcome}\n{ask_name}"
    
    def movie_list_response(self, movies):
        """Generate list of all movies"""
        output = "Currently showing:\n\n"
        for i, (key, movie) in enumerate(movies.items(), 1):
            output += f"{i}. {movie['title']} ({movie['rating']})\n"
            output += f"   Genre: {movie['genre'].capitalize()}, Duration: {movie['duration']}\n"
            output += f"   Price: £{movie['price']:.2f}\n"
        output += "\nWhat would you like to know more about?"
        return output
    
    def movie_info_response(self, movie):
        """Generate detailed movie information"""
        intro = self.generator.movie_info_intro(movie['title'])
        
        details = f"\n{intro}\n\n"
        details += f"🎬 Title: {movie['title']}\n"
        details += f"🎭 Genre: {movie['genre'].capitalize()}\n"
        details += f"⭐ Rating: {movie['rating']}\n"
        details += f"⏱️  Duration: {movie['duration']}\n"
        details += f"🎥 Director: {movie['director']}\n"
        details += f"👥 Cast: {', '.join(movie['cast'])}\n\n"
        details += f"📖 Description: {movie['description']}\n\n"
        details += f"🕐 Showtimes: {', '.join(movie['times'])}\n"
        details += f"💷 Price: £{movie['price']:.2f} per ticket\n\n"
        details += "Would you like to book tickets for this movie?"
        
        return details
    
    def booking_start_response(self, movie):
        """Generate booking start message"""
        start_msg = self.generator.booking_start(movie['title'])
        ask_time = self.generator.ask_time()
        
        output = f"{start_msg}\n\n"
        output += f"Available times: {', '.join(movie['times'])}\n\n"
        output += ask_time
        
        return output
    
    def time_selected_response(self, time):
        """Generate time selection confirmation"""
        ask_tickets = self.generator.ask_tickets()
        return f"Perfect! {time} showing selected.\n\n{ask_tickets} (1-10)"
    
    def tickets_selected_response(self, num, seat_map):
        """Generate ticket selection confirmation"""
        ask_seats = self.generator.ask_seats(num)
        
        output = seat_map
        output += f"\n\nYou're booking {num} ticket(s).\n"
        output += ask_seats
        output += "\nFormat: A1, B5, C3"
        
        return output
    
    def booking_summary(self, movie, time, tickets, seats, total):
        """Generate booking summary for confirmation"""
        seats_str = Helper.format_seat_list(seats)
        prompt = self.generator.confirmation_prompt()
        
        summary = "\n" + "="*60 + "\n"
        summary += "                    BOOKING SUMMARY\n"
        summary += "="*60 + "\n\n"
        summary += f"🎬 Movie: {movie['title']}\n"
        summary += f"🕐 Time: {time}\n"
        summary += f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y')}\n"
        summary += f"🎟️  Tickets: {tickets}\n"
        summary += f"💺 Seats: {seats_str}\n"
        summary += f"💷 Price: £{movie['price']:.2f} x {tickets} = £{total:.2f}\n\n"
        summary += "="*60 + "\n\n"
        summary += f"{prompt}\n\n"
        summary += "Type 'yes' to confirm or 'no' to cancel."
        
        return summary
    
    def confirmation_message(self, ref, name, movie, time, seats, tickets, total):
        """Generate booking confirmation message"""
        seats_str = Helper.format_seat_list(seats)
        confirmed_msg = self.generator.booking_confirmed(ref)
        
        output = "\n" + "="*60 + "\n"
        output += "                  BOOKING CONFIRMED!\n"
        output += "="*60 + "\n\n"
        output += f"✅ {confirmed_msg}\n"
        output += f"👤 Customer: {name}\n\n"
        output += f"🎬 Movie: {movie['title']}\n"
        output += f"🕐 Time: {time} on {datetime.now().strftime('%A, %B %d')}\n"
        output += f"💺 Seats: {seats_str}\n"
        output += f"🎟️  Tickets: {tickets}\n"
        output += f"💷 Total: £{total:.2f}\n\n"
        output += "="*60 + "\n\n"
        output += "📧 Confirmation email sent!\n"
        output += "📱 Please show this reference at the cinema.\n"
        output += "🍿 Enjoy your movie!\n\n"
        output += self.generator.how_can_help()
        
        return output
    
    def cancellation_message(self):
        """Generate cancellation message"""
        cancel_msg = self.generator.cancel()
        how_help = self.generator.how_can_help()
        return f"❌ {cancel_msg}\n\n{how_help}"
    
    def help_message(self, in_booking=False, stage=None):
        """Generate help message"""
        if in_booking and stage:
            stage_help = {
                'time': "Select a showtime from the available times shown above.",
                'tickets': "Enter the number of tickets you need (1-10).",
                'seats': "Select seats using format: A1, B5, C3",
                'confirm': "Type 'yes' to confirm your booking or 'no' to cancel."
            }
            help_text = f"ℹ️  Current step: {stage_help.get(stage, 'Booking in progress')}\n\n"
            help_text += "💡 Type 'back' to go to previous step\n"
            help_text += "❌ Type 'cancel' to cancel booking"
            return help_text
        
        return """ℹ️  Available commands:

📽️  'show movies' - See what's playing
ℹ️  'tell me about [movie]' - Get movie information  
🎟️  'book [movie]' - Book tickets
❓ 'what is my name' - I'll tell you your name
📋 'my bookings' - View booking history
❓ 'help' - Show this message
👋 'quit' - Exit

You can also type naturally! Just tell me what you want."""
    
    def bookings_list_response(self, bookings, name):
        """Generate bookings list"""
        if not bookings:
            return f"You don't have any bookings yet, {name}.\n\nWould you like to book a movie?"
        
        output = f"📋 Your Booking History ({len(bookings)} booking(s)):\n\n"
        
        for i, booking in enumerate(bookings, 1):
            seats_str = Helper.format_seat_list([tuple(s) for s in booking['seats']])
            output += f"{i}. 🎬 {booking['movie_title']}\n"
            output += f"   🔖 Reference: {booking['reference']}\n"
            output += f"   🕐 Time: {booking['time']}\n"
            output += f"   💺 Seats: {seats_str}\n"
            output += f"   🎟️  Tickets: {booking['tickets']}\n"
            output += f"   💷 Total: £{booking['total']:.2f}\n"
            output += f"   📅 Date: {Helper.format_datetime(booking['timestamp'])}\n\n"
        
        return output
    
    def error_message(self, custom_message=None):
        """Generate error message"""
        if custom_message:
            return f"⚠️  {custom_message}"
        return self.generator.error()
    
    def validation_error(self, message):
        """Generate validation error"""
        return f"⚠️  {message}"

if __name__ == "__main__":
    print("✅ NLGManager module loaded successfully!")
    
    # Quick test
    nlg = NLGManager()
    
    print("\n🧪 Quick Test:")
    print(nlg.welcome_message())
    print("\n" + "─"*50)
    print(nlg.welcome_message("Alice"))