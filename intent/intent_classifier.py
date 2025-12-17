import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
from config import INTENT_MODEL_FILE, INTENT_CONFIDENCE_THRESHOLD
from utils.text_processor import TextProcessor

class IntentClassifier:
    # Set up the ML intent classifier and load or train the model
    def __init__(self):
        self.text_processor = TextProcessor()
        self.vectorizer = None
        self.classifier = None
        self.load_or_train()
    
    # Try to load an existing model, otherwise train a new one
    def load_or_train(self):
        if not self.load_model():
            from .intent_trainer import IntentTrainer
            trainer = IntentTrainer()
            self.vectorizer, self.classifier = trainer.train()
            self.save_model()
    
    # Return the predicted intent label and confidence for some text
    def classify(self, text):
        if not text or not text.strip():
            return 'unknown', 0.0
        
        try:
            processed = self.text_processor.stem_text(text)
            
            text_vector = self.vectorizer.transform([processed])
            
            intent = self.classifier.predict(text_vector)[0]
            probs = self.classifier.predict_proba(text_vector)[0]
            confidence = max(probs)
            
            if confidence < INTENT_CONFIDENCE_THRESHOLD:
                return 'unknown', confidence
            
            return intent, confidence
            
        except Exception as e:
            print(f"Classification error: {e}")
            return 'unknown', 0.0
    
    # Save the trained model to disk
    def save_model(self):
        with open(INTENT_MODEL_FILE, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'classifier': self.classifier
            }, f)
        print(f"Model saved to {INTENT_MODEL_FILE}")
    
    # Load a previously trained model from disk
    def load_model(self):
        with open(INTENT_MODEL_FILE, 'rb') as f:
            data = pickle.load(f)
            self.vectorizer = data['vectorizer']
            self.classifier = data['classifier']
        # print(f"Model loaded from {INTENT_MODEL_FILE}")
        return True


if __name__ == "__main__":
    pass
    # print("IntentClassifier module loaded successfully!")
    