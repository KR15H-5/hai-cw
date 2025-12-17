import random
from datetime import datetime
from .templates import Templates

class ResponseGenerator:
    
    # Create a generator with access to all NLG templates
    def __init__(self):
        self.templates = Templates()
    
    # Pick a random template and format it with any extra values
    def generate(self, template_list, **kwargs):
        template = random.choice(template_list)
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    
    # Build a welcome line using the greeting text
    def welcome(self, greeting):
        return self.generate(Templates.WELCOME, greeting=greeting)
    
    # Ask the user for their name
    def ask_name(self):
        return self.generate(Templates.ASK_NAME)
    
    # Greet a known user by name
    def greet_user(self, name):
        return self.generate(Templates.GREET_USER, name=name)
    
    # Ask how the bot can help the user
    def how_can_help(self):
        return self.generate(Templates.HOW_CAN_HELP)
    
    # Intro line before detailed movie information
    def movie_info_intro(self, title):
        return self.generate(Templates.MOVIE_INFO_INTRO, title=title)
    
    # Opening line when starting a booking for a movie
    def booking_start(self, title):
        return self.generate(Templates.BOOKING_START, title=title)
    
    # Ask the user which showtime they want
    def ask_time(self):
        return self.generate(Templates.ASK_TIME)
    
    # Ask how many tickets the user wants
    def ask_tickets(self):
        return self.generate(Templates.ASK_TICKETS)
    
    # Ask the user to choose specific seats
    def ask_seats(self, count):
        return self.generate(Templates.ASK_SEATS, count=count)
    
    # Prompt the user to confirm or cancel their booking
    def confirmation_prompt(self):
        return self.generate(Templates.CONFIRMATION_PROMPT)
    
    # Short message when a booking has been confirmed
    def booking_confirmed(self, ref):
        return self.generate(Templates.BOOKING_CONFIRMED, ref=ref)
    
    # Polite reply to thanks from the user
    def thanks(self):
        return self.generate(Templates.THANKS)
    
    # Generic error message for unexpected input
    def error(self):
        return self.generate(Templates.ERROR)
    
    # Light, positive small talk response
    def small_talk_positive(self):
        return self.generate(Templates.SMALL_TALK_POSITIVE)
    
    # Farewell message when the chat ends
    def goodbye(self):
        return self.generate(Templates.GOODBYE)
    
    # Message shown when cancelling a booking
    def cancel(self):
        return self.generate(Templates.CANCEL)
    
    # Message used when stepping back in a flow
    def go_back(self):
        return self.generate(Templates.GO_BACK)

if __name__ == "__main__":
    print("ResponseGenerator module loaded successfully!")