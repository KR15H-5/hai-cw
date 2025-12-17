#!/usr/bin/env python3

from core import MovieBot

# Print the decorative banner at the start of the program
def print_banner():
    banner = """
╔════════════════════════════════════════════════════════╗
║                                                        ║
║                SAVOYBOT ASSISTANT!                     ║
║                                                        ║
║                Your NLP Movie Booking Bot              ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
"""
    print(banner)

# Run the main interactive chat loop for the SavoyBot assistant
def main():
    print_banner()
    
    bot = MovieBot(user_id='user_001')
    
    print("SavoyBot:", bot.greet())
    print("\n" + "─" * 60 + "\n")
    
    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            response = bot.respond(user_input)
            
            if response is None:
                print("\nSavoyBot:", bot.nlg.generator.goodbye())
                print("\n" + "─" * 60)
                print("Thank you for using SavoyBot!")
                print("─" * 60 + "\n")
                break
            
            print(f"\nSavoyBot: {response}")
            print("\n" + "─" * 60 + "\n")
        
        except KeyboardInterrupt:
            print("\n\nSavoyBot:", bot.nlg.generator.goodbye())
            break
        
        except Exception as e:
            print(f"\nSavoyBot: Sorry, an error occurred: {str(e)}")
            print("Please try again or type 'help' for assistance.\n")

if __name__ == "__main__":
    main()