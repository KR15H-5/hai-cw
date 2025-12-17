import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from utils.text_processor import TextProcessor
from config import DATA_DIR

class IntentTrainer:
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.intent_data = self._load_training_data()
    
    def load_training_data(self):
        training_file = os.path.join(DATA_DIR, 'training_data.json')
        
        try:
            with open(training_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return self._get_fallback_data()
        except json.JSONDecodeError as e:
            return self._get_fallback_data()
    
    def get_fallback_data(self):
        return {
            'greeting': ['hello', 'hi', 'hey'],
            'farewell': ['bye', 'goodbye'],
            'help': ['help']
        }
    
    def train(self):

        X = []
        y = []
        
        for intent, examples in self.intent_data.items():
            for example in examples:
                processed = self.text_processor.stem_text(example)
                X.append(processed)
                y.append(intent)
        
        print(f"Training on {len(X)} examples across {len(self.intent_data)} intents")
        
        vectorizer = TfidfVectorizer(
            max_features=1000,  
            ngram_range=(1, 3), 
            min_df=1,
            sublinear_tf=True 
        )
        X_vec = vectorizer.fit_transform(X)
        
    
        classifier = LogisticRegression(
            max_iter=2000, 
            C=10.0,  
            random_state=42,
            solver='lbfgs',
            class_weight='balanced'  
        )
        classifier.fit(X_vec, y)
        
        train_accuracy = classifier.score(X_vec, y)
        print(f"Training complete - Accuracy: {train_accuracy*100:.2f}%")
        
        return vectorizer, classifier

if __name__ == "__main__":
    print("IntentTrainer module loaded successfully!")
    