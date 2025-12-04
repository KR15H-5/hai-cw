class QAKnowledge:
    """
    Knowledge base for FAQ
    Stores question-answer pairs and movie-specific patterns
    """
    
    @staticmethod
    def get_general_qa():
        """Get general FAQ question-answer pairs"""
        return {
            # Bot identity
            "what is your name": "I'm SavoyBot, your intelligent movie booking assistant!",
            "who are you": "I'm SavoyBot, your intelligent movie booking assistant!",
            "what are you": "I'm SavoyBot, an AI-powered chatbot designed to help you book movie tickets!",
            "who am i talking to": "You're talking to SavoyBot, your movie booking assistant!",
            "tell me about yourself": "I'm SavoyBot, your intelligent movie booking assistant!",
            "whats your name": "I'm SavoyBot, your intelligent movie booking assistant!",
            "your name": "I'm SavoyBot!",
            "who r u": "I'm SavoyBot, your intelligent movie booking assistant!",
            "what do you do": "I can help you browse movies, book tickets, check showtimes, view your bookings, and answer questions about our cinema.",
            
            # Movies
            "what movies are playing": "We have Captain America: Brave New World, Thunderbolts, Mission: Impossible, Superman, and The Fantastic Four currently showing. Type 'show movies' for full details!",
            "what movies do you have": "We have Captain America: Brave New World, Thunderbolts, Mission: Impossible, Superman, and The Fantastic Four currently showing.",
            "whats on": "We have Captain America: Brave New World, Thunderbolts, Mission: Impossible, Superman, and The Fantastic Four currently showing.",
            
            # Booking info
            "how do i book tickets": "Just tell me which movie you'd like to watch, and I'll guide you through selecting a time, number of tickets, and seats!",
            "what are the showtimes": "Showtimes vary by movie. Which movie are you interested in?",
            "how much are tickets": "Tickets range from £10.50 to £14.00 depending on the movie.",
            
            # Location & parking
            "where is the cinema": "Our cinema is located at 123 Savoy Street, Nottingham, NG1 1AA.",
            "cinema address": "123 Savoy Street, Nottingham, NG1 1AA.",
            "where are you located": "We're located at 123 Savoy Street, Nottingham, NG1 1AA.",
            "do you have parking": "Yes! We have free parking available for all customers in our underground car park.",
            "is there parking": "Yes! We have free underground parking for all customers.",
            "parking available": "Yes! Free underground parking is available.",
            "free parking": "Yes! We have free underground parking for all customers.",
            "where can i park": "We have free underground parking available for all customers.",
            
            # Hours
            "what time do you open": "We open 30 minutes before the first showing each day.",
            "opening hours": "We open 30 minutes before the first showing each day.",
            "when do you open": "We open 30 minutes before the first showing each day.",
            "what time do you close": "We close 30 minutes after the last showing ends.",
            "closing time": "We close 30 minutes after the last showing ends.",
            "when do you close": "We close 30 minutes after the last showing ends.",
            
            # Food & concessions
            "do you serve food": "Yes! We have a full concessions stand with popcorn, nachos, hot dogs, candy, and drinks.",
            "do you have food": "Yes! We have a full concessions stand with popcorn, nachos, hot dogs, candy, and drinks.",
            "can i buy food": "Yes! We have a full concessions stand with popcorn, nachos, hot dogs, candy, and drinks.",
            "do you sell popcorn": "Yes! We sell popcorn, candy, drinks, and other snacks at our concessions stand.",
            "can i bring my own food": "Outside food and drinks are not permitted, but we have a great selection at our concessions!",
            "outside food allowed": "Outside food and drinks are not permitted, but we have a great selection at our concessions!",
            "can i bring food": "Outside food and drinks are not permitted, but we have a great selection at our concessions!",
            "bring own snacks": "Outside food and drinks are not permitted, but we have a great selection at our concessions!",
            
            # 3D movies
            "do you have 3d movies": "Currently all our showings are in 2D, but we're planning to add 3D screens soon!",
            "do you show 3d": "Currently all our showings are in 2D, but we're planning to add 3D screens soon!",
            "3d available": "Currently all our showings are in 2D, but we're planning to add 3D screens soon!",
            "are there 3d movies": "Currently all our showings are in 2D, but we're planning to add 3D screens soon!",
            "3d movies": "Currently all our showings are in 2D, but we're planning to add 3D screens soon!",
            "any 3d": "Currently all our showings are in 2D, but we're planning to add 3D screens soon!",
            
            # Accessibility
            "wheelchair access": "Yes, we have full wheelchair access and accessible seating in all screens.",
            "disabled access": "Yes, we have full wheelchair access and accessible seating in all screens.",
            "accessibility": "Yes, we have full wheelchair access and accessible seating in all screens.",
            "is there wheelchair access": "Yes, we have full wheelchair access and accessible seating in all screens.",
            
            # Discounts
            "are there discounts": "We offer student discounts (20% off with valid ID) and family deals (4 tickets for £40).",
            "do you have discounts": "We offer student discounts (20% off with valid ID) and family deals (4 tickets for £40).",
            "student discount": "We offer 20% off for students with valid ID.",
            "family deal": "We offer a family deal: 4 tickets for £40!",
            "any deals": "We offer student discounts (20% off with valid ID) and family deals (4 tickets for £40).",
            
            # Cancellations & refunds
            "can i cancel my booking": "Bookings can be modified up to 1 hour before the showing. Contact us at 0115-123-4567.",
            "can i change my booking": "Bookings can be modified up to 1 hour before the showing. Contact us at 0115-123-4567.",
            "what is your refund policy": "Tickets can be refunded up to 2 hours before the showing. Contact us at bookings@savoybot.com",
            "refund policy": "Tickets can be refunded up to 2 hours before the showing. Contact us at bookings@savoybot.com",
            "can i get a refund": "Tickets can be refunded up to 2 hours before the showing. Contact us at bookings@savoybot.com",
            
            # Payment
            "what payment methods do you accept": "We accept all major credit/debit cards, contactless payments, and mobile wallets (Apple Pay, Google Pay).",
            "can i pay with card": "Yes! We accept all major credit/debit cards and contactless payments.",
            "payment methods": "We accept all major credit/debit cards, contactless payments, and mobile wallets.",
            "do you accept cash": "Yes, we accept both cash and card payments.",
            
            # Gift cards
            "do you have gift cards": "Yes! Gift cards are available at the box office in denominations from £10 to £100.",
            "gift cards": "Yes! Gift cards are available at the box office in denominations from £10 to £100.",
            "gift card": "Yes! Gift cards are available at the box office in denominations from £10 to £100.",
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

if __name__ == "__main__":
    print("QAKnowledge module loaded successfully!")
