import random
from datetime import datetime
from .templates import Templates

class ResponseGenerator:
    
    def __init__(self):
        self.templates = Templates()
    
    def generate(self, template_list, **kwargs):
        template = random.choice(template_list)
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    
    def welcome(self, greeting):
        return self.generate(Templates.WELCOME, greeting=greeting)
    
    def ask_name(self):
        return self.generate(Templates.ASK_NAME)
    
    def greet_user(self, name):
        return self.generate(Templates.GREET_USER, name=name)
    
    def how_can_help(self):
        return self.generate(Templates.HOW_CAN_HELP)
    
    def movie_info_intro(self, title):
        return self.generate(Templates.MOVIE_INFO_INTRO, title=title)
    
    def booking_start(self, title):
        return self.generate(Templates.BOOKING_START, title=title)
    
    def ask_time(self):
        return self.generate(Templates.ASK_TIME)
    
    def ask_tickets(self):
        return self.generate(Templates.ASK_TICKETS)
    
    def ask_seats(self, count):
        return self.generate(Templates.ASK_SEATS, count=count)
    
    def confirmation_prompt(self):
        return self.generate(Templates.CONFIRMATION_PROMPT)
    
    def booking_confirmed(self, ref):
        return self.generate(Templates.BOOKING_CONFIRMED, ref=ref)
    
    def thanks(self):
        return self.generate(Templates.THANKS)
    
    def error(self):
        return self.generate(Templates.ERROR)
    
    def small_talk_positive(self):
        return self.generate(Templates.SMALL_TALK_POSITIVE)
    
    def goodbye(self):
        return self.generate(Templates.GOODBYE)
    
    def cancel(self):
        return self.generate(Templates.CANCEL)
    
    def go_back(self):
        return self.generate(Templates.GO_BACK)

if __name__ == "__main__":
    print("ResponseGenerator module loaded successfully!")