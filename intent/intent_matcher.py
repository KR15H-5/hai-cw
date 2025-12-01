import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .intent_classifier import IntentClassifier
from .intent_rules import IntentRules

class IntentMatcher:
    """
    Main intent matching orchestrator
    Combines rule-based and ML approaches
    """
    
    def __init__(self):
        self.rules = IntentRules()
        self.classifier = IntentClassifier()
    
    def match(self, text):
        """
        Match user intent using rules first, then ML
        Returns: (intent, confidence)
        """
        # Try rule-based first (high confidence)
        rule_intent = self.rules.check(text)
        if rule_intent:
            return rule_intent, 1.0
        
        # Fall back to ML classifier
        ml_intent, confidence = self.classifier.classify(text)
        return ml_intent, confidence
    
    def get_intent_with_context(self, text, context):
        """
        Get intent considering conversational context
        Args:
            text: User input
            context: Context dictionary with state info
        Returns: (intent, confidence)
        """
        # First get base intent
        intent, confidence = self.match(text)
        
        # Context-aware intent modification
        # Check if awaiting confirmation (e.g., after showing movie info)
        if context.get('awaiting_confirmation'):
            text_lower = text.lower().strip()
            
            # Check for affirmative responses
            if any(word in text_lower for word in ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay']):
                return 'confirm_booking', 1.0
            
            # Check for negative responses
            elif any(word in text_lower for word in ['no', 'nope', 'nah', 'cancel']):
                return 'cancel_booking', 1.0
        
        # Check if in booking stage
        booking_stage = context.get('booking_state', {}).get('stage')
        if booking_stage:
            text_lower = text.lower().strip()
            
            # Check for cancel keywords
            if text_lower in ['cancel', 'stop', 'quit', 'exit', 'abort']:
                return 'cancel_booking', 1.0
            
            # Check for go back keywords
            if text_lower in ['back', 'go back', 'previous', 'undo']:
                return 'go_back', 1.0
        
        # Return original intent if no context override
        return intent, confidence

if __name__ == "__main__":
    print("✅ IntentMatcher module loaded successfully!")
    
    # Quick test
    matcher = IntentMatcher()
    
    test_phrases = [
        "hello there",
        "I want to book dune",
        "show me movies",
        "how much is it",
        "what is my name",
        "thanks a lot"
    ]
    
    print("\n🧪 Quick Test:")
    for phrase in test_phrases:
        intent, confidence = matcher.match(phrase)
        print(f"   '{phrase}' → {intent} ({confidence:.2f})")