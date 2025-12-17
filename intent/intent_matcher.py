import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .intent_classifier import IntentClassifier

class IntentMatcher:
    
    # Create a matcher that wraps the ML classifier
    def __init__(self):
        self.classifier = IntentClassifier()
    
    # Run the raw classifier on text and return its intent prediction
    def match(self, text):
        ml_intent, confidence = self.classifier.classify(text)
        return ml_intent, confidence
    
    # Adjust the intent based on conversation context rules
    def get_intent_with_context(self, text, context):
        intent, confidence = self.match(text)
        
        if context.get('awaiting_confirmation'):
            text_lower = text.lower().strip()
            
            if any(word in text_lower for word in ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay']):
                return 'confirm_booking', 1.0
            
            elif any(word in text_lower for word in ['no', 'nope', 'nah', 'cancel']):
                return 'cancel_booking', 1.0
        
        booking_stage = context.get('booking_state', {}).get('stage')
        if booking_stage:
            text_lower = text.lower().strip()
            
            if text_lower in ['cancel', 'stop', 'quit', 'exit', 'abort']:
                return 'cancel_booking', 1.0
            
            if text_lower in ['back', 'go back', 'previous', 'undo']:
                return 'go_back', 1.0
        
        return intent, confidence

if __name__ == "__main__":
    print("IntentMatcher module loaded successfully!")
    