import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.validators import Validator

print("\n🧪 Testing Validator Module...")
print("="*60)

# Test 1: Validate seat
print("\n1️⃣ Testing validate_seat()...")
is_valid, error = Validator.validate_seat('A', 5)
assert is_valid == True
print("   ✅ Valid seat A5 accepted")

is_valid, error = Validator.validate_seat('Z', 5)
assert is_valid == False
print(f"   ✅ Invalid seat Z5 rejected: {error}")

is_valid, error = Validator.validate_seat('A', 15)
assert is_valid == False
print(f"   ✅ Invalid seat A15 rejected: {error}")

# Test 2: Validate ticket count
print("\n2️⃣ Testing validate_ticket_count()...")
is_valid, error = Validator.validate_ticket_count(5)
assert is_valid == True
print("   ✅ Valid ticket count 5 accepted")

is_valid, error = Validator.validate_ticket_count(0)
assert is_valid == False
print(f"   ✅ Invalid ticket count 0 rejected: {error}")

is_valid, error = Validator.validate_ticket_count(15)
assert is_valid == False
print(f"   ✅ Invalid ticket count 15 rejected: {error}")

# Test 3: Validate time
print("\n3️⃣ Testing validate_time()...")
available_times = ['14:00', '17:30', '20:00']
is_valid, time = Validator.validate_time('1400', available_times)
assert is_valid == True
assert time == '14:00'
print(f"   ✅ Valid time 1400 matched to {time}")

is_valid, time = Validator.validate_time('14:00', available_times)
assert is_valid == True
print(f"   ✅ Valid time 14:00 accepted")

is_valid, time = Validator.validate_time('15:00', available_times)
assert is_valid == False
print("   ✅ Invalid time 15:00 rejected")

# Test 4: Validate email
print("\n4️⃣ Testing validate_email()...")
assert Validator.validate_email('test@example.com') == True
print("   Valid email 'test@example.com' accepted")

assert Validator.validate_email('user@uni.ac.uk') == True
print("   Valid email 'user@uni.ac.uk' accepted")

assert Validator.validate_email('invalid-email') == False
print("   Invalid email rejected")

# Test 5: Validate phone
print("\n5️⃣ Testing validate_phone()...")
assert Validator.validate_phone('07123456789') == True
print("    Valid phone '07123456789' accepted")

assert Validator.validate_phone('+447123456789') == True
print("   Valid phone '+447123456789' accepted")

assert Validator.validate_phone('123') == False
print("   Invalid phone '123' rejected")

print("\n" + "="*60)
print("ALL VALIDATOR TESTS PASSED!")
print("="*60)