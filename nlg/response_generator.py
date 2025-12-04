import random
from datetime import datetime
from .templates import Templates

class ResponseGenerator:
    """
    Generates natural language responses from templates
    Handles template selection and variable substitution
    """
    
    def __init__(self):
        self.templates = Templates()
    
    def generate(self, template_list, **kwargs):
        """
        Generate response from template list
        Args:
            template_list: List of template strings
            **kwargs: Variables to substitute in template
        Returns: Generated response string
        """
        template = random.choice(template_list)
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    
    def welcome(self, greeting):
        """Generate welcome message"""
        return self.generate(Templates.WELCOME, greeting=greeting)
    
    def ask_name(self):
        """Ask for user's name"""
        return self.generate(Templates.ASK_NAME)
    
    def greet_user(self, name):
        """Greet user by name"""
        return self.generate(Templates.GREET_USER, name=name)
    
    def how_can_help(self):
        """Ask how to help"""
        return self.generate(Templates.HOW_CAN_HELP)
    
    def movie_info_intro(self, title):
        """Movie info introduction"""
        return self.generate(Templates.MOVIE_INFO_INTRO, title=title)
    
    def booking_start(self, title):
        """Start booking process"""
        return self.generate(Templates.BOOKING_START, title=title)
    
    def ask_time(self):
        """Ask for showtime"""
        return self.generate(Templates.ASK_TIME)
    
    def ask_tickets(self):
        """Ask for number of tickets"""
        return self.generate(Templates.ASK_TICKETS)
    
    def ask_seats(self, count):
        """Ask for seat selection"""
        return self.generate(Templates.ASK_SEATS, count=count)
    
    def confirmation_prompt(self):
        """Prompt for confirmation"""
        return self.generate(Templates.CONFIRMATION_PROMPT)
    
    def booking_confirmed(self, ref):
        """Booking confirmation message"""
        return self.generate(Templates.BOOKING_CONFIRMED, ref=ref)
    
    def thanks(self):
        """Thank you response"""
        return self.generate(Templates.THANKS)
    
    def error(self):
        """Error message"""
        return self.generate(Templates.ERROR)
    
    def small_talk_positive(self):
        """Response to 'how are you'"""
        return self.generate(Templates.SMALL_TALK_POSITIVE)
    
    def goodbye(self):
        """Goodbye message"""
        return self.generate(Templates.GOODBYE)
    
    def cancel(self):
        """Cancellation message"""
        return self.generate(Templates.CANCEL)
    
    def go_back(self):
        """Go back message"""
        return self.generate(Templates.GO_BACK)

if __name__ == "__main__":
    print("ResponseGenerator module loaded successfully!")