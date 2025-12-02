import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from context import ContextManager
from intent import IntentMatcher
from nlg import NLGManager
from qa import QAManager
from transaction import TransactionManager
from utils.text_processor import TextProcessor
from .session import Session  # ← FIXED: Changed from "from core import MovieBot"

class MovieBot:
    """
    Main Movie Booking Bot
    Orchestrates all components to handle user conversations
    """
    
    def __init__(self, user_id='default_user'):
        self.user_id = user_id
        self.session = Session(user_id)
        
        self.db = DatabaseManager()
        self.context = ContextManager(user_id)
        self.intent_matcher = IntentMatcher()
        self.nlg = NLGManager()
        self.qa = QAManager(self.db)
        self.transaction = TransactionManager(self.db)
        self.text_processor = TextProcessor()
        
        self.last_question_was_name = False
        
        booking_state = self.context.get_booking_state()
        if booking_state.get('stage') and not booking_state.get('movie'):
            print("⚠️  Detected corrupt booking state, cleaning...")
            self.context.reset_booking()
    
    def greet(self):
        """Initial greeting"""
        name = self.context.get('name')
        self.last_question_was_name = (name is None)
        return self.nlg.welcome_message(name)
    
    def respond(self, user_input):
        """
        Main response method
        Processes user input and generates appropriate response
        """
        self.session.update_activity()
        
        if not user_input or not user_input.strip():
            return "I didn't catch that. Could you say that again?"
        
        text_lower = user_input.lower().strip()
        
        # Check for quit commands
        if text_lower in ['quit', 'exit', 'bye', 'goodbye']:
            return None
        
        # Handle name input if just asked for name
        if self.last_question_was_name:
            # Try to extract name
            name = self.text_processor.extract_name(user_input)
            
            if name:
                self.context.set('name', name)
                self.last_question_was_name = False
                response = self.nlg.welcome_message(name)
                self.context.add_to_history(user_input, response)
                return response
            
            # If extraction failed but it's a short input, treat as direct name
            words = user_input.split()
            if len(words) <= 2 and not any(word in text_lower for word in ['what', 'show', 'help', 'movie', 'book']):
                name = words[0].capitalize()
                self.context.set('name', name)
                self.last_question_was_name = False
                response = self.nlg.welcome_message(name)
                self.context.add_to_history(user_input, response)
                return response
            
            # Otherwise process normally
            self.last_question_was_name = False
        
        # Handle booking stages
        booking_state = self.context.get_booking_state()
        stage = booking_state.get('stage')
        
        if stage:
            response = self._handle_booking_stage(user_input, stage)
            self.context.add_to_history(user_input, response)
            return response
        
        # Handle awaiting confirmation
        if self.context.get('awaiting_confirmation'):
            response = self._handle_awaiting_confirmation(user_input)
            self.context.add_to_history(user_input, response)
            return response
        
        # Get intent
        intent, confidence = self.intent_matcher.get_intent_with_context(
            user_input,
            self.context.context
        )

        print(f"🔍 DEBUG: Intent='{intent}', Confidence={confidence:.2f}")

        
        # Route based on intent
        response = self._route_intent(intent, user_input)
        self.context.add_to_history(user_input, response)
        return response
    
    def _handle_name_input(self, text):
        """Handle simple name input"""
        if len(text.split()) <= 2 and not any(word in text.lower() for word in ['book', 'movie', 'show', 'help']):
            name = self.text_processor.extract_name(text)
            if name:
                self.context.set('name', name)
                self.last_question_was_name = False
                return self.nlg.welcome_message(name)
        return None
    
    def _handle_booking_stage(self, user_input, stage):
        """Handle input during booking flow"""
        text_lower = user_input.lower().strip()
        
        # Check for back/cancel
        if text_lower in ['back', 'go back']:
            return self._handle_go_back()
        
        if text_lower in ['cancel', 'stop']:
            return self._handle_cancel()
        
        # Route to appropriate stage handler
        if stage == 'time':
            return self._handle_time_selection(user_input)
        elif stage == 'tickets':
            return self._handle_ticket_selection(user_input)
        elif stage == 'seats':
            return self._handle_seat_selection(user_input)
        elif stage == 'confirm':
            return self._handle_confirmation(user_input)
        
        return self.nlg.error_message()
    
    def _handle_time_selection(self, time_input):
        """Handle showtime selection"""
        booking_state = self.context.get_booking_state()
        movie_key = booking_state['movie']
        movie = self.db.get_movie(movie_key)
        
        time, error = self.transaction.validate_time(movie, time_input)
        
        if error:
            return self.nlg.validation_error(error)
        
        self.context.update_booking_state({'time': time, 'stage': 'tickets'})
        return self.nlg.time_selected_response(time)
    
    def _handle_ticket_selection(self, num_input):
        """Handle ticket count selection"""
        num, error = self.transaction.validate_tickets(num_input)
        
        if error:
            return self.nlg.validation_error(error)
        
        booking_state = self.context.get_booking_state()
        movie_key = booking_state['movie']
        showtime = booking_state['time']
        
        seat_map = self.transaction.show_seat_map(movie_key, showtime)
        
        self.context.update_booking_state({'tickets': num, 'stage': 'seats'})
        return self.nlg.tickets_selected_response(num, seat_map)
    
    def _handle_seat_selection(self, seat_input):
        """Handle seat selection"""
        booking_state = self.context.get_booking_state()
        movie_key = booking_state['movie']
        showtime = booking_state['time']
        num_tickets = booking_state['tickets']
        
        seats, error = self.transaction.validate_seats(
            seat_input, movie_key, showtime, num_tickets
        )
        
        if error:
            return self.nlg.validation_error(error)
        
        movie = self.db.get_movie(movie_key)
        total = self.transaction.calculate_total(movie, num_tickets)
        
        self.context.update_booking_state({'seats': seats, 'stage': 'confirm'})
        
        return self.nlg.booking_summary(movie, showtime, num_tickets, seats, total)
    
    def _handle_confirmation(self, user_input):
        """Handle booking confirmation"""
        text_lower = user_input.lower()
        
        if any(word in text_lower for word in ['yes', 'confirm', 'ok', 'yeah', 'yep']):
            return self._confirm_booking()
        elif any(word in text_lower for word in ['no', 'cancel', 'nope']):
            return self._handle_cancel()
        else:
            return "Please type 'yes' to confirm or 'no' to cancel the booking."
    
    def _confirm_booking(self):
        """Confirm and create booking"""
        booking_state = self.context.get_booking_state()
        user_name = self.context.get('name', 'Guest')
        
        movie_key = booking_state['movie']
        showtime = booking_state['time']
        num_tickets = booking_state['tickets']
        seats = booking_state['seats']
        
        movie = self.db.get_movie(movie_key)
        total = self.transaction.calculate_total(movie, num_tickets)
        
        ref = self.transaction.confirm_booking(
            self.user_id, user_name, movie_key, showtime, num_tickets, seats, total
        )
        
        response = self.nlg.confirmation_message(
            ref, user_name, movie, showtime, seats, num_tickets, total
        )
        
        self.context.reset_booking()
        
        return response
    
    def _handle_awaiting_confirmation(self, user_input):
        """Handle awaiting booking confirmation after showing movie info"""
        text_lower = user_input.lower()
        
        if any(word in text_lower for word in ['yes', 'yeah', 'yep', 'sure', 'ok', 'book']):
            self.context.set('awaiting_confirmation', False)
            last_movie = self.context.get('last_mentioned_movie')
            if last_movie:
                return self._start_booking(last_movie)
        elif any(word in text_lower for word in ['no', 'nope', 'cancel']):
            self.context.set('awaiting_confirmation', False)
            return "Okay. " + self.nlg.generator.how_can_help()
        
        return "Would you like to book this movie? (yes/no)"
    
    def _handle_go_back(self):
        """Handle going back in booking flow"""
        booking_state = self.context.get_booking_state()
        stage = booking_state.get('stage')
        
        stages = ['time', 'tickets', 'seats', 'confirm']
        
        if not stage or stage not in stages:
            return "Nothing to go back to."
        
        current_idx = stages.index(stage)
        
        if current_idx == 0:
            return "Already at the first step. Type 'cancel' to start over."
        
        previous_stage = stages[current_idx - 1]
        
        if previous_stage == 'time':
            self.context.update_booking_state({
                'stage': 'time',
                'time': None,
                'tickets': None,
                'seats': []
            })
            movie = self.db.get_movie(booking_state['movie'])
            return f"⬅️  Going back...\n\nWhich showtime? Available: {', '.join(movie['times'])}"
        
        elif previous_stage == 'tickets':
            self.context.update_booking_state({
                'stage': 'tickets',
                'tickets': None,
                'seats': []
            })
            return "⬅️  Going back...\n\nHow many tickets? (1-10)"
        
        elif previous_stage == 'seats':
            self.context.update_booking_state({
                'stage': 'seats',
                'seats': []
            })
            seat_map = self.transaction.show_seat_map(
                booking_state['movie'],
                booking_state['time']
            )
            return f"⬅️  Going back...\n\n{seat_map}\n\nPlease select your {booking_state['tickets']} seat(s)."
        
        return "Something went wrong. Type 'cancel' to start over."
    
    def _handle_cancel(self):
        """Cancel booking"""
        self.context.reset_booking()
        return self.nlg.cancellation_message()
    
    def _route_intent(self, intent, user_input):
        """Route to appropriate handler based on intent"""
        name = self.context.get('name')
        
        if intent == 'greeting':
            if name:
                return f"Hello again, {name}! " + self.nlg.generator.how_can_help()
            return self.greet()
        
        elif intent == 'farewell':
            return None
        
        elif intent == 'give_name':
            return self._handle_give_name(user_input)
        
        elif intent == 'change_name':
            return self._handle_change_name()
        elif intent == 'ask_name':
            return self._handle_ask_name()
        
        elif intent == 'small_talk_positive':
            return self.nlg.generator.small_talk_positive() + " Ready to help you book some great movies!"
        
        elif intent == 'small_talk_thanks':
            return self.nlg.generator.thanks()
        
        elif intent == 'show_movies':
            movie_key = self._find_movie(user_input)
            if movie_key:
                return self._show_movie_info(movie_key)
            return self._show_all_movies()
        
        elif intent == 'movie_info':
            return self._handle_movie_info_request(user_input)
        
        elif intent == 'book_tickets':
            return self._handle_book_request(user_input)
        
        elif intent == 'view_bookings':
            return self._show_bookings()
        
        elif intent == 'help':
            booking_state = self.context.get_booking_state()
            return self.nlg.help_message(
                booking_state.get('stage') is not None,
                booking_state.get('stage')
            )
        
        elif intent == 'ask_price':
            return self._handle_price_query(user_input)
        
        elif intent == 'ask_time':
            return self._handle_time_query(user_input)
        
        elif intent == 'praise':
            return "Thank you! I'm glad you're enjoying the experience! 🎉"
        
        elif intent == 'complaint':
            return "I'm sorry you're experiencing issues. Please contact our support team at support@cinebook.com"
        
        # Try QA system
        qa_answer = self.qa.find_answer(user_input)
        if qa_answer:
            return qa_answer
        
        # Try finding movie
        movie_key = self._find_movie(user_input)
        if movie_key:
            return self._show_movie_info(movie_key)
        
        return self.nlg.error_message("I'm not sure what you mean. Type 'help' for options or 'show movies' to see what's playing.")
    
    def _handle_give_name(self, text):
        """Handle user giving their name"""
        name = self.text_processor.extract_name(text)
        if name:
            self.context.set('name', name)
            self.last_question_was_name = False
            return self.nlg.welcome_message(name)
        return "Sorry, I didn't catch your name. Could you repeat it?"
    
    def _handle_ask_name(self):
        """Handle user asking about their name"""
        name = self.context.get('name')
        if name:
            return f"Your name is {name}."
        return "You haven't told me your name yet."
    
    def _show_all_movies(self):
        """Show all available movies"""
        movies = self.db.get_all_movies()
        return self.nlg.movie_list_response(movies)
    
    def _show_movie_info(self, movie_key):
        """Show information about a specific movie"""
        movie = self.db.get_movie(movie_key)
        if not movie:
            return "Sorry, I couldn't find that movie."
        
        self.context.set('last_mentioned_movie', movie_key)
        self.context.set('awaiting_confirmation', True)
        
        return self.nlg.movie_info_response(movie)
    
    def _handle_movie_info_request(self, user_input):
        """Handle request for movie information"""
        movie_key = self._find_movie(user_input)
        
        if movie_key:
            movie = self.db.get_movie(movie_key)
            movie_answer = self.qa.get_movie_answer(user_input, movie)
            if movie_answer:
                return movie_answer
            return self._show_movie_info(movie_key)
        
        return "Which movie would you like to know about?\n\n" + self._show_all_movies()
    
    def _handle_book_request(self, user_input):
        """Handle booking request"""
        movie_key = self._find_movie(user_input)
        
        if movie_key:
            return self._start_booking(movie_key)
        
        return "Which movie would you like to book?\n\n" + self._show_all_movies()
    
    def _start_booking(self, movie_key):
        """Start booking process"""
        movie, error = self.transaction.start_booking(movie_key)
        
        if error:
            return self.nlg.error_message(error)
        
        self.context.update_booking_state({
            'stage': 'time',
            'movie': movie_key,
            'time': None,
            'tickets': None,
            'seats': []
        })
        
        return self.nlg.booking_start_response(movie)
    
    def _show_bookings(self):
        """Show user's booking history"""
        bookings = self.db.get_user_bookings(self.user_id)
        name = self.context.get('name', 'Guest')
        return self.nlg.bookings_list_response(bookings, name)
    
    def _handle_price_query(self, user_input):
        """Handle price query"""
        movie_key = self._find_movie(user_input)
        
        if movie_key:
            movie = self.db.get_movie(movie_key)
            return f"Tickets for {movie['title']} cost £{movie['price']:.2f} each."
        
        return "Most tickets are £12.50, but family films like Paddington are £10.00."
    
    def _handle_time_query(self, user_input):
        """Handle showtime query"""
        movie_key = self._find_movie(user_input)
        
        if movie_key:
            movie = self.db.get_movie(movie_key)
            return f"{movie['title']} is showing at: {', '.join(movie['times'])}"
        
        return "Showtimes vary by movie. Which movie are you interested in?"
    
    def _find_movie(self, query):
        """Find movie from user query"""
        query_lower = query.lower()
        
        keywords = {
            'captain america': 'captain_america',
            'captain': 'captain_america',
            'thunderbolts': 'thunderbolts',
            'mission impossible': 'mission_impossible',
            'mission': 'mission_impossible',
            'tom cruise': 'mission_impossible',
            'superman': 'superman',
            'fantastic four': 'fantastic_four',
            'fantastic': 'fantastic_four',
            'ff': 'fantastic_four'
        }
        
        for keyword, movie_key in keywords.items():
            if keyword in query_lower:
                return movie_key
        
        results = self.db.search_movies(query)
        if results:
            return results[0][0]
        
        return None
    def _handle_change_name(self):
        """Handle user wanting to change their name"""
        self.last_question_was_name = True
        return "Sure! What would you like me to call you?"

if __name__ == "__main__":
    print("✅ MovieBot module loaded successfully!")