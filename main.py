#!/usr/bin/env python3

from core import MovieBot

def print_banner():
    """Print welcome banner"""
    banner = """
╔════════════════════════════════════════════════════════╗
║                                                        ║
║                SAVOY CINEMA ASSISTANT!                 ║
║                                                        ║
║                Your NLP Movie Booking Bot              ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """Main application loop"""
    print_banner()
    
    # Create bot instance
    bot = MovieBot(user_id='user_001')
    
    # Initial greeting
    print("Bot:", bot.greet())
    print("\n" + "─" * 60 + "\n")
    
    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            response = bot.respond(user_input)
            
            if response is None:
                print("\nBot:", bot.nlg.generator.goodbye())
                print("\n" + "─" * 60)
                print("Thank you for using CineBook! 🎬🍿")
                print("─" * 60 + "\n")
                break
            
            print(f"\nBot: {response}")
            print("\n" + "─" * 60 + "\n")
        
        except KeyboardInterrupt:
            print("\n\nBot:", bot.nlg.generator.goodbye())
            break
        
        except Exception as e:
            print(f"\nBot: Sorry, an error occurred: {str(e)}")
            print("Please try again or type 'help' for assistance.\n")

if __name__ == "__main__":
    main()