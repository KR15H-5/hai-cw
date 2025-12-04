import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
from config import INTENT_MODEL_FILE, INTENT_CONFIDENCE_THRESHOLD
from utils.text_processor import TextProcessor

class IntentClassifier:
    """
    ML-based intent classifier
    Uses trained Logistic Regression model
    """
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.vectorizer = None
        self.classifier = None
        self.load_or_train()
    
    def load_or_train(self):
        """Load existing model or train new one"""
        if not self.load_model():
            print("📚 No existing model found. Training new model...")
            from .intent_trainer import IntentTrainer
            trainer = IntentTrainer()
            self.vectorizer, self.classifier = trainer.train()
            self.save_model()
    
    def classify(self, text):
        """
        Classify user intent
        Returns: (intent, confidence)
        """
        if not text or not text.strip():
            return 'unknown', 0.0
        
        try:
            # Preprocess text
            processed = self.text_processor.stem_text(text)
            
            # Vectorize
            text_vec = self.vectorizer.transform([processed])
            
            # Predict
            intent = self.classifier.predict(text_vec)[0]
            probs = self.classifier.predict_proba(text_vec)[0]
            confidence = max(probs)
            
            # Check confidence threshold
            if confidence < INTENT_CONFIDENCE_THRESHOLD:
                return 'unknown', confidence
            
            return intent, confidence
            
        except Exception as e:
            print(f"⚠️  Classification error: {e}")
            return 'unknown', 0.0
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            with open(INTENT_MODEL_FILE, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'classifier': self.classifier
                }, f)
            print(f"💾 Model saved to {INTENT_MODEL_FILE}")
        except Exception as e:
            print(f"⚠️  Could not save model: {e}")
    
    def load_model(self):
        """Load trained model from disk"""
        try:
            with open(INTENT_MODEL_FILE, 'rb') as f:
                data = pickle.load(f)
                self.vectorizer = data['vectorizer']
                self.classifier = data['classifier']
            print(f"✅ Model loaded from {INTENT_MODEL_FILE}")
            return True
        except Exception as e:
            return False

if __name__ == "__main__":
    print("IntentClassifier module loaded successfully!")
    