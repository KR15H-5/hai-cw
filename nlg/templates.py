class Templates:
    """
    Response templates for natural language generation
    Each template type has multiple variations for naturalness
    """
    
    WELCOME = [
        "{greeting}. Welcome to SavoyBot!",
        "{greeting}! Welcome to SavoyBot, your movie booking assistant!",
        "{greeting}. Thanks for choosing SavoyBot!",
        "{greeting}. SavoyBot here, ready to help you book amazing movies!"
    ]
    
    ASK_NAME = [
        "What's your name?",
        "May I have your name, please?",
        "What should I call you?",
        "Could you tell me your name?"
    ]
    
    GREET_USER = [
        "Nice to meet you, {name}!",
        "Hello, {name}! Great to meet you!",
        "Welcome, {name}!",
        "Pleasure to meet you, {name}!",
        "Hi {name}! So glad you're here!"
    ]
    
    HOW_CAN_HELP = [
        "How can I help you today?",
        "What can I do for you?",
        "How may I assist you?",
        "What would you like to do today?",
        "What brings you here today?"
    ]
    
    MOVIE_INFO_INTRO = [
        "Here's what I know about {title}:",
        "Let me tell you about {title}:",
        "{title} - here are the details:",
        "Great choice! Here's the info on {title}:"
    ]
    
    BOOKING_START = [
        "Great! Let's book {title} for you.",
        "Excellent choice! Booking {title}.",
        "Perfect! Let's get you tickets for {title}.",
        "Wonderful! I'll help you book {title}."
    ]
    
    ASK_TIME = [
        "Which showtime works for you?",
        "What time would you prefer?",
        "Which time slot would you like?",
        "When would you like to watch?"
    ]
    
    ASK_TICKETS = [
        "How many tickets do you need?",
        "How many tickets would you like?",
        "For how many people?",
        "How many seats should I reserve?"
    ]
    
    ASK_SEATS = [
        "Please select your {count} seat(s).",
        "Which seats would you like?",
        "Choose your {count} seat(s) please.",
        "Pick {count} seat(s) from the map above."
    ]
    
    CONFIRMATION_PROMPT = [
        "Does this look good to you?",
        "Ready to confirm?",
        "Is everything correct?",
        "Shall I confirm this booking?",
        "Everything look good?"
    ]
    
    BOOKING_CONFIRMED = [
        "Booking confirmed! Your reference is {ref}.",
        "All set! Here's your booking reference: {ref}.",
        "Done! Your booking reference is {ref}.",
        "Success! Reference number: {ref}."
    ]
    
    THANKS = [
        "You're welcome!",
        "Happy to help!",
        "My pleasure!",
        "Anytime!",
        "Glad I could help!"
    ]
    
    ERROR = [
        "Sorry, I didn't quite get that.",
        "I'm not sure I understand.",
        "Could you rephrase that?",
        "Can you say that differently?"
    ]
    
    SMALL_TALK_POSITIVE = [
        "I'm doing well, thank you!",
        "I'm great, thanks for asking!",
        "Doing fantastic! Ready to help you book movies!",
        "I'm wonderful! How can I help you today?"
    ]
    
    GOODBYE = [
        "Goodbye! Thanks for using CineBook!",
        "See you soon! Enjoy your movie!",
        "Take care! Come back anytime!",
        "Farewell! Happy movie watching!"
    ]
    
    CANCEL = [
        "Booking cancelled. No charges made.",
        "Alright, booking cancelled.",
        "No problem, I've cancelled that for you.",
        "Cancelled. No worries!"
    ]
    
    GO_BACK = [
        "Going back...",
        "Okay, let's go back.",
        "Taking you back to the previous step.",
        "Alright, going backwards."
    ]

if __name__ == "__main__":
    print("Templates module loaded successfully!")
    print(f"\nAvailable template sets: {len([attr for attr in dir(Templates) if attr.isupper()])}")