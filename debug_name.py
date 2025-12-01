from core import MovieBot

bot = MovieBot('debug_user')

# IMPORTANT: Call greet first to set last_question_was_name = True
print("Bot:", bot.greet())
print("\n" + "="*60 + "\n")

# Test name extraction
test_inputs = [
    "My name is TestUser",
    "TestUser",
]

for inp in test_inputs:
    print(f"Input: '{inp}'")
    response = bot.respond(inp)
    print(f"Response: {response[:100]}...")  # Truncate long responses
    print(f"Stored name: {bot.context.get('name')}")
    print()