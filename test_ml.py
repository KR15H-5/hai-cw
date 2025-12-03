#!/usr/bin/env python3
"""
Test ML Model Training
"""

from intent import IntentTrainer, IntentClassifier

print("\n" + "="*70)
print("🧪 ML MODEL TRAINING TEST")
print("="*70)

# Train the model
print("\n📚 Training ML model from scratch...")
trainer = IntentTrainer()
vectorizer, classifier = trainer.train()

print(f"\n✅ Training complete!")
print(f"📊 Model type: {type(classifier).__name__}")
print(f"📊 Total intents: {len(classifier.classes_)}")
print(f"📊 Intents: {', '.join(classifier.classes_)}")

# Save the model
from intent.intent_classifier import IntentClassifier
ic = IntentClassifier()
ic.vectorizer = vectorizer
ic.classifier = classifier
ic.save_model()
print(f"\n💾 Model saved!")

# Test the model
print("\n" + "="*70)
print("🧪 TESTING ML MODEL")
print("="*70)

test_cases = [
    "hello",
    "hi there",
    "good morning",
    "how are you",
    "how are you doing",
    "i want to book tickets",
    "book a movie",
    "show me movies",
    "what movies are playing",
    "thanks",
    "thank you",
    "bye",
    "goodbye",
    "what is my name",
    "tell me about dune",
    "my bookings",
]

print("\n")
for text in test_cases:
    intent, confidence = ic.classify(text)
    emoji = "✅" if confidence > 0.5 else "⚠️" if confidence > 0.3 else "❌"
    print(f"{emoji} '{text}' → {intent} (confidence: {confidence:.2f})")

print("\n" + "="*70)
print("✅ ML MODEL TEST COMPLETE")
print("="*70 + "\n")