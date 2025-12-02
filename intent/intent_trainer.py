import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from utils.text_processor import TextProcessor
from config import DATA_DIR

class IntentTrainer:
    """
    Trains the intent classification model
    Loads training data from JSON file
    """
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.intent_data = self._load_training_data()
    
    def _load_training_data(self):
        """Load training data from JSON file"""
        training_file = os.path.join(DATA_DIR, 'training_data.json')
        
        try:
            with open(training_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Loaded training data from {training_file}")
            return data
        except FileNotFoundError:
            print(f"❌ Training data file not found: {training_file}")
            print("   Using minimal fallback data...")
            return self._get_fallback_data()
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            print("   Using minimal fallback data...")
            return self._get_fallback_data()
    
    def _get_fallback_data(self):
        """Minimal fallback data if JSON fails"""
        return {
            'greeting': ['hello', 'hi', 'hey'],
            'farewell': ['bye', 'goodbye'],
            'help': ['help']
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
            max_features=1000,  # Increased from 500
            ngram_range=(1, 3),  # Increased to trigrams
            min_df=1,
            sublinear_tf=True  # Use sublinear term frequency
        )
        X_vec = vectorizer.fit_transform(X)
        
        # Train Logistic Regression classifier
        classifier = LogisticRegression(
            max_iter=2000,  # Increased iterations
            C=10.0,  # Increased regularization parameter
            random_state=42,
            solver='lbfgs',
            class_weight='balanced'  # Handle class imbalance
        )
        classifier.fit(X_vec, y)
        
        # Calculate accuracy on training set
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