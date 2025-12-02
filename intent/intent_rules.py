class IntentRules:
    """
    Rule-based intent matching
    Catches high-confidence patterns before ML
    """
    
    def check(self, text):
        """
        Check text against rule-based patterns
        Returns: intent or None
        """
        text_lower = text.lower().strip()

        if text_lower == 'help':
            return 'help'
        # if self._is_change_name(text_lower):
        #     return 'change_name'
        
        # if self._is_ask_name(text_lower):
        #     return 'ask_name'
        
        # if self._is_small_talk_positive(text_lower):
        #     return 'small_talk_positive'
        
        # if self._is_book_intent(text_lower):
        #     return 'book_tickets'
        
        # if self._is_price_query(text_lower):
        #     return 'ask_price'
        
        # if self._is_thanks(text_lower):
        #     return 'small_talk_thanks'
        
        # if self._is_greeting(text_lower):
        #     return 'greeting'
        
        # if self._is_show_movies(text_lower):
        #     return 'show_movies'
        
        return None
    
    def _is_ask_name(self, text):
        """Check if asking about name"""
        if 'your' in text or 'you' in text:
            return False
        return 'name' in text and ('my' in text or 'what' in text or 'whats' in text)

    def _is_change_name(self, text):
        """Check if wanting to change name"""
        return ('change' in text or 'update' in text) and 'name' in text
    
    def _is_small_talk_positive(self, text):
        """Check if asking how are you"""
        phrases = ['how are you', 'how r u', 'how are u', 'hows it going', 'how you doing']
        return any(phrase in text for phrase in phrases)
    
    def _is_book_intent(self, text):
        """Check if booking intent"""
        return 'book' in text or 'reserve' in text
    
    def _is_price_query(self, text):
        """Check if asking about price"""
        return 'price' in text or 'cost' in text or 'how much' in text
    
    def _is_thanks(self, text):
        """Check if thanking"""
        return any(word in text for word in ['thank', 'thanks', 'thx'])
    
    def _is_greeting(self, text):
        """Check if greeting (only for short inputs)"""
        greetings = ['hello', 'hi', 'hey', 'hiya']
        words = text.split()
        return len(words) <= 2 and any(g in words for g in greetings)
    
    def _is_show_movies(self, text):
        """Check if asking to show movies"""
        phrases = ['show movies', 'list movies', 'what movies', 'whats playing']
        return any(phrase in text for phrase in phrases)

if __name__ == "__main__":
    print("✅ IntentRules module loaded successfully!")
    
    # Quick test
    rules = IntentRules()
    
    test_cases = [
        ("what is my name", "ask_name"),
        ("how are you", "small_talk_positive"),
        ("book tickets", "book_tickets"),
        ("thanks", "small_talk_thanks"),
        ("hi", "greeting"),
    ]
    
    print("\n🧪 Quick Test:")
    for text, expected in test_cases:
        result = rules.check(text)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{text}' → {result} (expected: {expected})")