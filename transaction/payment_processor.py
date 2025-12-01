class PaymentProcessor:
    """
    Handles payment calculations and processing
    """
    
    def calculate_total(self, movie, num_tickets):
        """Calculate total price for booking"""
        return movie['price'] * num_tickets
    
    def process(self, amount, payment_method='card'):
        """
        Process payment (simulated)
        Returns: (success, message)
        """
        return True, f"Payment of £{amount:.2f} processed successfully via {payment_method}"
    
    def validate_payment_method(self, method):
        """Validate payment method"""
        valid_methods = ['card', 'cash', 'mobile']
        return method.lower() in valid_methods
    
    def calculate_discount(self, total, discount_type=None):
        """Calculate discounted price"""
        if discount_type == 'student':
            return total * 0.8  # 20% off
        elif discount_type == 'family':
            return min(total, 40.0)  # Family deal: max £40
        elif discount_type == 'senior':
            return total * 0.85  # 15% off
        return total
    
    def format_price(self, price):
        """Format price for display"""
        return f"£{price:.2f}"

if __name__ == "__main__":
    print("✅ PaymentProcessor module loaded successfully!")
    
    # Quick test
    processor = PaymentProcessor()
    
    print("\n🧪 Quick Test:")
    
    test_movie = {'price': 12.50}
    total = processor.calculate_total(test_movie, 3)
    print(f"3 tickets at £12.50 = {processor.format_price(total)}")
    
    discounted = processor.calculate_discount(total, 'student')
    print(f"With student discount = {processor.format_price(discounted)}")