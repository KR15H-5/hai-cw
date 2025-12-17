class PaymentProcessor:
    
    def calculate_total(self, movie, num_tickets):
        return movie['price'] * num_tickets
    
    def process(self, amount, payment_method='card'):
        return True, f"Payment of £{amount:.2f} processed successfully via {payment_method}"
    
    def validate_payment_method(self, method):
        valid_methods = ['card', 'cash', 'mobile']
        return method.lower() in valid_methods
    
    def calculate_discount(self, total, discount_type=None):
        if discount_type == 'student':
            return total * 0.8  
        elif discount_type == 'family':
            return min(total, 40.0) 
        elif discount_type == 'senior':
            return total * 0.85  
        return total
    
    def format_price(self, price):
        return f"£{price:.2f}"

if __name__ == "__main__":
    print("PaymentProcessor module loaded successfully!")
    