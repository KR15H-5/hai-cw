import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from utils.text_processor import TextProcessor

class IntentTrainer:
    """
    Trains the intent classification model
    Uses extensive training data for better accuracy
    """
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.intent_data = self._get_training_data()
    
    def _get_training_data(self):
        """
        Comprehensive training data for all intents
        Each intent has multiple example phrases
        """
        return {
            'greeting': [
                'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
                'greetings', 'howdy', 'whats up', 'sup', 'yo', 'hiya', 'heya', 'greetings',
                'hi there', 'hello there', 'hey there', 'good day', 'morning', 'evening'
            ],
            
            'farewell': [
                'bye', 'goodbye', 'see you', 'farewell', 'take care', 'catch you later',
                'see ya', 'later', 'peace out', 'have a good day', 'talk to you later',
                'bye bye', 'good night', 'see you soon', 'until next time', 'ciao'
            ],
            
            'give_name': [
                'my name is john', 'i am sarah', 'call me mike', 'im alex', "i'm chris",
                'this is david', 'you can call me emma', 'they call me sam',
                'my name is alice', 'i am bob', 'call me charlie', 'im diana',
                'the name is eric', 'people call me frank', 'i go by george'
            ],
            
            'ask_name': [
                'what is my name', 'whats my name', 'tell me my name', 'my name',
                'do you know my name', 'who am i', 'what do you call me', 'remind me my name',
                'what did i say my name was', 'can you tell me my name'
            ],
            
            'small_talk_positive': [
                'how are you', 'how are you doing', 'hows it going', 'how do you do',
                'how have you been', 'whats up with you', 'hows life', 'how r u', 'how are things',
                'hows your day', 'how are you today', 'how is everything', 'whats new',
                'how you doing', 'you good', 'you alright', 'everything ok'
            ],
            
            'small_talk_thanks': [
                'thank you', 'thanks', 'thx', 'appreciate it', 'cheers', 'thanks a lot',
                'thank you so much', 'many thanks', 'thanks so much', 'appreciated',
                'thank you very much', 'much appreciated', 'thanks very much', 'ta',
                'thank you kindly', 'thanks again'
            ],
            
            'show_movies': [
                'show movies', 'list movies', 'what movies', 'available movies', 'whats playing',
                'what is playing', 'movies showing', 'which movies', 'see movies', 'display movies',
                'movie list', 'show me movies', 'what movies are on', 'whats on',
                'what films are showing', 'show me whats playing', 'list all movies',
                'what can i watch', 'what movies do you have', 'show films'
            ],
            
            'movie_info': [
                'tell me about dune', 'info about joker', 'information about paddington',
                'describe the movie', 'details about the film', 'explain the plot',
                'what is it about', 'who stars in it', 'who directed it', 'what is the movie about',
                'tell me more about', 'give me details on', 'information on', 'describe',
                'what can you tell me about', 'i want to know about', 'whats the story'
            ],
            
            'book_tickets': [
                'book', 'reserve', 'buy tickets', 'get tickets', 'purchase tickets',
                'want tickets', 'book tickets', 'make reservation', 'i want to book',
                'id like to book', 'can i book', 'reserve seats', 'get me tickets',
                'i want to watch', 'id like to see', 'book me', 'reserve for me',
                'i need tickets', 'purchase', 'buy', 'get seats'
            ],
            
            'help': [
                'help', 'what can you do', 'options', 'commands', 'how do i',
                'assist me', 'guide me', 'show me how', 'what are your capabilities',
                'help me', 'i need help', 'how does this work', 'what do you do',
                'can you help', 'show options', 'what can i do', 'how to use'
            ],
            
            'confirm': [
                'yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'confirm', 'correct',
                'right', 'proceed', 'go ahead', 'affirmative', 'absolutely', 'definitely',
                'thats right', 'sounds good', 'alright', 'fine', 'agreed', 'yup',
                'aye', 'indeed', 'certainly', 'of course', 'for sure'
            ],
            
            'deny': [
                'no', 'nope', 'nah', 'not really', 'negative', 'dont think so',
                'i dont think so', 'not interested', 'no thanks', 'no thank you',
                'naw', 'nay', 'no way', 'not at all', 'definitely not'
            ],
            
            'cancel': [
                'cancel', 'stop', 'nevermind', 'abort', 'forget it', 'dont want to',
                'changed my mind', 'cancel booking', 'stop this', 'end this',
                'quit', 'exit', 'never mind', 'forget about it', 'i dont want'
            ],
            
            'go_back': [
                'back', 'go back', 'previous', 'undo', 'return', 'go to previous step',
                'previous step', 'step back', 'take me back', 'go backwards',
                'revert', 'back up', 'previous screen'
            ],
            
            'view_bookings': [
                'my bookings', 'show bookings', 'booking history', 'view bookings',
                'past bookings', 'previous bookings', 'my reservations', 'booking list',
                'what did i book', 'my tickets', 'show my bookings', 'list my bookings',
                'reservation history', 'my orders', 'order history'
            ],
            
            'ask_price': [
                'how much', 'what is the price', 'cost', 'ticket price', 'how much does it cost',
                'price', 'how expensive', 'what does it cost', 'whats the cost', 'ticket cost',
                'how much is it', 'what is the cost', 'pricing', 'how much are tickets',
                'whats the price', 'price per ticket'
            ],
            
            'ask_time': [
                'what time', 'when', 'showtimes', 'show times', 'screening times',
                'when is it showing', 'at what time', 'what times', 'available times',
                'when can i watch', 'screening schedule', 'time slots', 'when does it start',
                'what time is the movie'
            ],
            
            'complaint': [
                'this is bad', 'not good', 'terrible', 'awful', 'disappointed',
                'doesnt work', 'broken', 'problem', 'issue', 'not working', 'poor service',
                'this sucks', 'horrible', 'useless', 'frustrated', 'annoying', 'error'
            ],
            
            'praise': [
                'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'awesome',
                'brilliant', 'perfect', 'love it', 'very good', 'outstanding', 'superb',
                'incredible', 'spectacular', 'marvelous', 'terrific', 'impressive'
            ]
        }
    
    def train(self):
        """
        Train the intent classification model
        Returns: (vectorizer, classifier)
        """
        X = []
        y = []
        
        # Prepare training data
        for intent, examples in self.intent_data.items():
            for example in examples:
                # Stem the text for better generalization
                processed = self.text_processor.stem_text(example)
                X.append(processed)
                y.append(intent)
        
        print(f"🎓 Training on {len(X)} examples across {len(self.intent_data)} intents...")
        
        # Vectorize using TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=500, 
            ngram_range=(1, 2),  # Use both unigrams and bigrams
            min_df=1
        )
        X_vec = vectorizer.fit_transform(X)
        
        # Train Logistic Regression classifier
        classifier = LogisticRegression(
            max_iter=1000, 
            C=1.0, 
            random_state=42,
            multi_class='multinomial'
        )
        classifier.fit(X_vec, y)
        
        # Calculate accuracy on training set (just for info)
        train_accuracy = classifier.score(X_vec, y)
        print(f"✅ Training complete! Accuracy: {train_accuracy*100:.2f}%")
        
        return vectorizer, classifier

if __name__ == "__main__":
    print("✅ IntentTrainer module loaded successfully!")
    
    # Quick test
    trainer = IntentTrainer()
    print(f"\n🧪 Quick Test:")
    print(f"Total intents: {len(trainer.intent_data)}")
    print(f"Intents: {list(trainer.intent_data.keys())}")
    
    total_examples = sum(len(examples) for examples in trainer.intent_data.values())
    print(f"Total training examples: {total_examples}")