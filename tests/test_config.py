import config
import os

print("\n🧪 Testing Config Module...")
print("="*50)

# Test 1: Check directories exist
assert os.path.exists(config.DATA_DIR), "❌ Data directory not created"
print("✅ Data directory exists")

assert os.path.exists(config.MODELS_DIR), "❌ Models directory not created"
print("✅ Models directory exists")

# Test 2: Check constants
assert config.SEATS_PER_ROW == 10, "❌ SEATS_PER_ROW incorrect"
print("✅ SEATS_PER_ROW correct")

assert config.ROWS == ['A', 'B', 'C', 'D', 'E'], "❌ ROWS incorrect"
print("✅ ROWS correct")

assert config.MAX_TICKETS == 10, "❌ MAX_TICKETS incorrect"
print("✅ MAX_TICKETS correct")

print("\n" + "="*50)
print("✅ ALL CONFIG TESTS PASSED!")
print("="*50)