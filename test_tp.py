import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.text_processor import TextProcessor

print("\n🧪 Testing TextProcessor Module...")
print("="*50)

processor = TextProcessor()

# Test 1: Clean text
text = "Hello, World! 123"
cleaned = processor.clean_text(text)
assert cleaned == "hello world 123"
print(f"✅ Clean text: '{text}' → '{cleaned}'")

# Test 2: Tokenize
tokens = processor.tokenize("I want to book tickets")
assert tokens == ['i', 'want', 'to', 'book', 'tickets']
print(f"✅ Tokenize: {tokens}")

# Test 3: Stem text
stemmed = processor.stem_text("I am booking tickets")
print(f"✅ Stem text: 'I am booking tickets' → '{stemmed}'")

# Test 4: Extract name
name = processor.extract_name("My name is John")
assert name == "John"
print(f"✅ Extract name: {name}")

name2 = processor.extract_name("I'm Sarah")
assert name2 == "Sarah"
print(f"✅ Extract name: {name2}")

# Test 5: Extract number
num = processor.extract_number("I want 5 tickets")
assert num == 5
print(f"✅ Extract number: {num}")

num2 = processor.extract_number("I need three tickets")
assert num2 == 3
print(f"✅ Extract word number: {num2}")

# Test 6: Parse seats
seats = processor.parse_seats("A1, B5, C3")
assert seats == [('A', 1), ('B', 5), ('C', 3)]
print(f"✅ Parse seats: {seats}")

print("\n" + "="*50)
print("✅ ALL TEXT PROCESSOR TESTS PASSED!")
print("="*50)