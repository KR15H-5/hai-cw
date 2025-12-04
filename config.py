import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

MOVIES_FILE = os.path.join(DATA_DIR, 'movies.json')
CONTEXT_FILE = os.path.join(DATA_DIR, 'context.json')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.json')
INTENT_MODEL_FILE = os.path.join(MODELS_DIR, 'intent_model.pkl')

SEATS_PER_ROW = 10
ROWS = ['A', 'B', 'C', 'D', 'E']
TICKET_PRICE = 12.50
MAX_TICKETS = 10
MIN_TICKETS = 1

INTENT_CONFIDENCE_THRESHOLD = 0.5
SIMILARITY_THRESHOLD = 0.25

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

print("Config loaded successfully!")
print(f"Data directory: {DATA_DIR}")
print(f"Models directory: {MODELS_DIR}")