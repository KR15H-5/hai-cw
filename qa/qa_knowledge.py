class QAKnowledge:
    """
    Knowledge base for FAQ
    Stores question-answer pairs and movie-specific patterns
    """
    
    @staticmethod
    def get_general_qa():
        """Get general FAQ question-answer pairs"""
        return {
            "what movies are playing": "We have Joker: Folie a Deux, Dune: Part Two, and Paddington in Peru currently showing.",
            "what is your name": "I'm SavoyBot, your intelligent movie booking assistant!",
            "what can you do": "I can help you browse movies, book tickets, check showtimes, view your bookings, and answer questions about our cinema.",
            "how do i book tickets": "Just tell me which movie you'd like to watch, and I'll guide you through selecting a time, number of tickets, and seats!",
            "what are the showtimes": "Showtimes vary by movie. Which movie are you interested in?",
            "how much are tickets": "Tickets vary by movie. Which movie are you interested in?",
            "can i cancel my booking": "Currently, bookings cannot be cancelled through the chatbot. Please contact the cinema at 0115-123-4567.",
            "where is the cinema": "Our cinema is located at 123 Movie Street, Nottingham, NG1 1AA.",
            "do you have parking": "Yes! We have free parking available for all customers in our underground car park.",
            "are there discounts": "We offer student discounts (20% off with valid ID) and family deals (4 tickets for £40).",
            "what is your refund policy": "Tickets can be refunded up to 2 hours before the showing. Contact us at bookings@SavoyBot.com",
            "do you serve food": "Yes! We have a full concessions stand with popcorn, nachos, hot dogs, candy, and drinks.",
            "what time do you open": "We open 30 minutes before the first showing each day.",
            "what time do you close": "We close 30 minutes after the last showing ends.",
            "do you have 3d movies": "Currently all our showings are in 2D, but we're planning to add 3D screens soon!",
            "is there wheelchair access": "Yes, we have full wheelchair access and accessible seating in all screens.",
            "can i bring my own food": "Outside food and drinks are not permitted, but we have a great selection at our concessions!",
            "do you have gift cards": "Yes! Gift cards are available at the box office in denominations from £10 to £100.",
            "what payment methods do you accept": "We accept all major credit/debit cards, contactless payments, and mobile wallets.",
            "can i change my booking": "Bookings can be modified up to 1 hour before the showing. Contact us at 0115-123-4567."
        }
    
    @staticmethod
    def get_movie_specific_patterns():
        """Get patterns for movie-specific questions"""
        return {
            'genre': "is a {genre} film.",
            'director': "was directed by {director}.",
            'cast': "stars {cast}.",
            'time': "is showing at: {times}.",
            'price': "costs £{price:.2f} per ticket.",
            'rating': "is rated {rating}.",
            'duration': "runs for {duration}.",
            'plot': "{description}"
        }

    @staticmethod
    def get_general_qa():
        """Get general FAQ question-answer pairs"""
        return {
            "what is your name": "I'm SavoyBot, your intelligent movie booking assistant!",
            "who are you": "I'm SavoyBot, your intelligent movie booking assistant!",
            "what are you": "I'm SavoyBot, an AI-powered chatbot designed to help you book movie tickets!",
            "who am i talking to": "You're talking to SavoyBot, your movie booking assistant!",
            "tell me about yourself": "I'm SavoyBot, your intelligent movie booking assistant!",
            "whats your name": "I'm SavoyBot, your intelligent movie booking assistant!",
            "your name": "I'm SavoyBot!",
            "who r u": "I'm SavoyBot, your intelligent movie booking assistant!",
            "what do you do": "I can help you browse movies, book tickets, check showtimes, view your bookings, and answer questions about our cinema.",
        }
if __name__ == "__main__":
    print("✅ QAKnowledge module loaded successfully!")
    
    # Quick test
    qa_pairs = QAKnowledge.get_general_qa()
    patterns = QAKnowledge.get_movie_specific_patterns()
    
    print(f"\n🧪 Quick Test:")
    print(f"General QA pairs: {len(qa_pairs)}")
    print(f"Movie patterns: {len(patterns)}")