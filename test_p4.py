#!/usr/bin/env python3
"""
Phase 4 Complete Test - Context, Transaction & QA
Run: python test_phase4_complete.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("🧪 PHASE 4: CONTEXT, TRANSACTION & QA - COMPLETE TEST SUITE")
print("="*70)

# Test 1: Memory Store
print("\n" + "─"*70)
print("💾 TEST 1: MEMORY STORE")
print("─"*70)

try:
    from context.memory_store import MemoryStore
    
    store = MemoryStore()
    
    # Test: Create new context
    new_ctx = store.create_new_context('test_user_1')
    assert new_ctx['user_id'] == 'test_user_1'
    assert new_ctx['name'] is None
    assert 'booking_state' in new_ctx
    print("   ✅ create_new_context() working")
    
    # Test: Load context
    ctx = store.load_context('test_user_1')
    assert ctx['user_id'] == 'test_user_1'
    print("   ✅ load_context() working")
    
    # Test: Save context
    ctx['name'] = 'TestUser'
    store.save_context('test_user_1', ctx)
    print("   ✅ save_context() working")
    
    # Test: Reload and verify
    reloaded = store.load_context('test_user_1')
    assert reloaded['name'] == 'TestUser'
    print("   ✅ Context persisted correctly")
    
    print("✅ MemoryStore: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ MemoryStore FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: State Tracker
print("\n" + "─"*70)
print("📊 TEST 2: STATE TRACKER")
print("─"*70)

try:
    from context.state_tracker import StateTracker
    
    tracker = StateTracker()
    test_ctx = {}
    
    # Test: Get empty state
    state = tracker.get_state(test_ctx)
    assert state['stage'] is None
    print("   ✅ get_state() returns empty state")
    
    # Test: Update state
    tracker.update_state(test_ctx, {'stage': 'time', 'movie': 'test_movie'})
    assert tracker.get_stage(test_ctx) == 'time'
    print("   ✅ update_state() working")
    
    # Test: Check if in booking
    assert tracker.is_in_booking(test_ctx) == True
    print("   ✅ is_in_booking() working")
    
    # Test: Get progress
    progress = tracker.get_progress(test_ctx)
    assert progress == 25  # time is first stage (1/4)
    print(f"   ✅ get_progress() = {progress}%")
    
    # Test: Set different stage
    tracker.set_stage(test_ctx, 'confirm')
    progress = tracker.get_progress(test_ctx)
    assert progress == 100
    print(f"   ✅ Progress at 'confirm' stage = {progress}%")
    
    # Test: Reset state
    tracker.reset_state(test_ctx)
    assert tracker.get_stage(test_ctx) is None
    assert tracker.is_in_booking(test_ctx) == False
    print("   ✅ reset_state() working")
    
    print("✅ StateTracker: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ StateTracker FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Context Manager
print("\n" + "─"*70)
print("🧠 TEST 3: CONTEXT MANAGER")
print("─"*70)

try:
    from context.context_manager import ContextManager
    
    ctx = ContextManager('test_user_ctx')
    
    # Test: Get/Set
    ctx.set('name', 'Alice')
    assert ctx.get('name') == 'Alice'
    print("   ✅ get() and set() working")
    
    # Test: Update multiple
    ctx.update({'name': 'Bob', 'preferences': {'language': 'en'}})
    assert ctx.get('name') == 'Bob'
    assert ctx.get('preferences')['language'] == 'en'
    print("   ✅ update() working")
    
    # Test: Booking state
    ctx.update_booking_state({'stage': 'tickets', 'movie': 'dune2'})
    state = ctx.get_booking_state()
    assert state['stage'] == 'tickets'
    assert state['movie'] == 'dune2'
    print("   ✅ update_booking_state() working")
    
    # Test: Check progress
    assert ctx.is_in_booking() == True
    progress = ctx.get_booking_progress()
    assert progress == 50  # tickets is 2nd stage (2/4)
    print(f"   ✅ Booking progress = {progress}%")
    
    # Test: Add to history
    ctx.add_to_history("hello", "Hi there!")
    history = ctx.get('conversation_history')
    assert len(history) > 0
    assert history[-1]['user'] == "hello"
    print("   ✅ add_to_history() working")
    
    # Test: Reset booking
    ctx.reset_booking()
    assert ctx.is_in_booking() == False
    assert ctx.get('awaiting_confirmation') == False
    print("   ✅ reset_booking() working")
    
    print("✅ ContextManager: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ ContextManager FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Payment Processor
print("\n" + "─"*70)
print("💳 TEST 4: PAYMENT PROCESSOR")
print("─"*70)

try:
    from transaction.payment_processor import PaymentProcessor
    
    processor = PaymentProcessor()
    
    # Test: Calculate total
    test_movie = {'price': 12.50}
    total = processor.calculate_total(test_movie, 3)
    assert total == 37.50
    print(f"   ✅ calculate_total(3 tickets): £{total:.2f}")
    
    # Test: Process payment
    success, msg = processor.process(37.50, 'card')
    assert success == True
    print(f"   ✅ process(): {msg}")
    
    # Test: Validate payment method
    assert processor.validate_payment_method('card') == True
    assert processor.validate_payment_method('invalid') == False
    print("   ✅ validate_payment_method() working")
    
    # Test: Discounts
    student_price = processor.calculate_discount(50.00, 'student')
    assert student_price == 40.00  # 20% off
    print(f"   ✅ Student discount: £50 → £{student_price:.2f}")
    
    family_price = processor.calculate_discount(60.00, 'family')
    assert family_price == 40.00  # Capped at £40
    print(f"   ✅ Family deal: £60 → £{family_price:.2f}")
    
    # Test: Format price
    formatted = processor.format_price(12.50)
    assert formatted == "£12.50"
    print(f"   ✅ format_price(): {formatted}")
    
    print("✅ PaymentProcessor: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ PaymentProcessor FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Booking Handler
print("\n" + "─"*70)
print("📝 TEST 5: BOOKING HANDLER")
print("─"*70)

try:
    from transaction.booking_handler import BookingHandler
    from database import DatabaseManager
    
    db = DatabaseManager()
    handler = BookingHandler(db)
    
    # Test: Start booking
    movie, error = handler.start('dune2')
    assert movie is not None
    assert movie['title'] == 'Dune: Part Two'
    print(f"   ✅ start('dune2'): {movie['title']}")
    
    movie, error = handler.start('invalid_movie')
    assert movie is None
    assert error is not None
    print(f"   ✅ start('invalid_movie'): Rejected")
    
    # Test: Validate time
    movie = db.get_movie('dune2')
    time, error = handler.validate_time(movie, '16:30')
    assert time == '16:30'
    assert error is None
    print(f"   ✅ validate_time('16:30'): Accepted")
    
    time, error = handler.validate_time(movie, '99:99')
    assert time is None
    assert error is not None
    print(f"   ✅ validate_time('99:99'): Rejected")
    
    # Test: Validate tickets
    num, error = handler.validate_tickets('5')
    assert num == 5
    assert error is None
    print(f"   ✅ validate_tickets('5'): {num}")
    
    num, error = handler.validate_tickets('15')
    assert num is None
    print(f"   ✅ validate_tickets('15'): Rejected")
    
    # Test: Show seat map
    seat_map = handler.show_seat_map('dune2', '16:30')
    assert 'SCREEN' in seat_map
    assert '✅' in seat_map or '❌' in seat_map
    print(f"   ✅ show_seat_map() generated")
    
    # Test: Validate seats
    seats, error = handler.validate_seats('E5, E6', 'paddington3', '11:00', 2)
    assert seats is not None
    assert len(seats) == 2
    print(f"   ✅ validate_seats('E5, E6'): {len(seats)} seats")
    
    seats, error = handler.validate_seats('A1', 'paddington3', '11:00', 2)
    assert seats is None  # Need 2 seats but only gave 1
    print(f"   ✅ validate_seats('A1') for 2 tickets: Rejected")
    
    print("✅ BookingHandler: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ BookingHandler FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Transaction Manager
print("\n" + "─"*70)
print("🔄 TEST 6: TRANSACTION MANAGER")
print("─"*70)

try:
    from transaction.transaction_manager import TransactionManager
    from database import DatabaseManager
    
    db = DatabaseManager()
    txn = TransactionManager(db)
    
    # Test: Start booking
    movie, error = txn.start_booking('joker2')
    assert movie is not None
    print(f"   ✅ start_booking('joker2'): {movie['title']}")
    
    # Test: Calculate total
    total = txn.calculate_total(movie, 2)
    assert total == movie['price'] * 2
    print(f"   ✅ calculate_total(2): £{total:.2f}")
    
    # Test: Confirm booking
    ref = txn.confirm_booking(
        'test_user_txn',
        'TestUser',
        'joker2',
        '14:00',
        2,
        [('C', 1), ('C', 2)],
        total
    )
    assert ref.startswith('BK')
    print(f"   ✅ confirm_booking(): {ref}")
    
    # Verify booking was saved
    booking = db.get_booking_by_reference(ref)
    assert booking is not None
    assert booking['reference'] == ref
    print(f"   ✅ Booking verified in database")
    
    print("✅ TransactionManager: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ TransactionManager FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: QA Knowledge
print("\n" + "─"*70)
print("📚 TEST 7: QA KNOWLEDGE BASE")
print("─"*70)

try:
    from qa.qa_knowledge import QAKnowledge
    
    knowledge = QAKnowledge()
    
    # Test: Get general QA
    qa_pairs = knowledge.get_general_qa()
    assert len(qa_pairs) > 0
    assert "what movies are playing" in qa_pairs
    print(f"   ✅ get_general_qa(): {len(qa_pairs)} QA pairs")
    
    # Test: Get movie patterns
    patterns = knowledge.get_movie_specific_patterns()
    assert 'genre' in patterns
    assert 'director' in patterns
    assert 'cast' in patterns
    print(f"   ✅ get_movie_specific_patterns(): {len(patterns)} patterns")
    
    print("✅ QAKnowledge: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ QAKnowledge FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 8: QA Retriever
print("\n" + "─"*70)
print("🔍 TEST 8: QA RETRIEVER")
print("─"*70)

try:
    from qa.qa_retriever import QARetriever
    from qa.qa_knowledge import QAKnowledge
    
    qa_pairs = QAKnowledge.get_general_qa()
    retriever = QARetriever(qa_pairs)
    
    # Test: Exact match
    answer, score = retriever.retrieve("what movies are playing")
    assert answer is not None
    assert score > 0.8  # High similarity
    print(f"   ✅ retrieve('what movies are playing'): Found (score: {score:.2f})")
    
    # Test: Similar query
    answer, score = retriever.retrieve("which movies are showing")
    assert answer is not None
    print(f"   ✅ retrieve('which movies are showing'): Found (score: {score:.2f})")
    
    # Test: Unrelated query
    answer, score = retriever.retrieve("xyz random nonsense")
    assert answer is None  # Below threshold
    print(f"   ✅ retrieve('xyz random nonsense'): None (score: {score:.2f})")
    
    print("✅ QARetriever: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ QARetriever FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 9: QA Manager
print("\n" + "─"*70)
print("💬 TEST 9: QA MANAGER")
print("─"*70)

try:
    from qa.qa_manager import QAManager
    from database import DatabaseManager
    
    db = DatabaseManager()
    qa = QAManager(db)
    
    # Test: General question
    answer = qa.find_answer("do you have parking")
    assert answer is not None
    assert "parking" in answer.lower()
    print(f"   ✅ find_answer('do you have parking'): Found")
    
    # Test: Movie-specific question
    movie = db.get_movie('dune2')
    
    answer = qa.get_movie_answer("who directed it", movie)
    assert answer is not None
    assert "Denis Villeneuve" in answer
    print(f"   ✅ get_movie_answer('who directed it'): {answer}")
    
    answer = qa.get_movie_answer("what genre", movie)
    assert answer is not None
    assert "sci-fi" in answer.lower()
    print(f"   ✅ get_movie_answer('what genre'): {answer}")
    
    answer = qa.get_movie_answer("how much", movie)
    assert answer is not None
    assert "12.50" in answer
    print(f"   ✅ get_movie_answer('how much'): Found price")
    
    print("✅ QAManager: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ QAManager FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 10: Integration Test
print("\n" + "─"*70)
print("🔗 TEST 10: FULL INTEGRATION TEST")
print("─"*70)

try:
    from context.context_manager import ContextManager
    from transaction.transaction_manager import TransactionManager
    from database import DatabaseManager
    
    print("\n   📖 Scenario: Complete booking with context tracking")
    
    # Setup
    db = DatabaseManager()
    ctx = ContextManager('integration_test_user')
    txn = TransactionManager(db)
    
    # Step 1: Set user name
    ctx.set('name', 'IntegrationTest')
    print(f"   1️⃣  User: {ctx.get('name')}")
    
    # Step 2: Start booking
    movie, _ = txn.start_booking('paddington3')
    ctx.update_booking_state({'stage': 'time', 'movie': 'paddington3'})
    print(f"   2️⃣  Started booking: {movie['title']}")
    print(f"      Progress: {ctx.get_booking_progress()}%")
    
    # Step 3: Select time
    time, _ = txn.validate_time(movie, '14:00')
    ctx.update_booking_state({'time': time, 'stage': 'tickets'})
    print(f"   3️⃣  Selected time: {time}")
    print(f"      Progress: {ctx.get_booking_progress()}%")
    
    # Step 4: Select tickets
    num, _ = txn.validate_tickets('2')
    ctx.update_booking_state({'tickets': num, 'stage': 'seats'})
    print(f"   4️⃣  Selected tickets: {num}")
    print(f"      Progress: {ctx.get_booking_progress()}%")
    
    # Step 5: Select seats
    seats, _ = txn.validate_seats('D1, D2', 'paddington3', '14:00', num)
    ctx.update_booking_state({'seats': seats, 'stage': 'confirm'})
    print(f"   5️⃣  Selected seats: {seats}")
    print(f"      Progress: {ctx.get_booking_progress()}%")
    
    # Step 6: Confirm booking
    total = txn.calculate_total(movie, num)
    ref = txn.confirm_booking(
        ctx.user_id,
        ctx.get('name'),
        'paddington3',
        time,
        num,
        seats,
        total
    )
    ctx.reset_booking()
    print(f"   6️⃣  Booking confirmed: {ref}")
    print(f"      Total: £{total:.2f}")
    print(f"      Progress after reset: {ctx.get_booking_progress()}%")
    
    # Verify booking
    booking = db.get_booking_by_reference(ref)
    assert booking is not None
    assert booking['user_id'] == ctx.user_id
    print(f"   ✅ Booking verified in database")
    
    # Verify seats are taken
    taken = db.get_taken_seats('paddington3', '14:00')
    for seat in seats:
        assert seat in taken
    print(f"   ✅ Seats marked as taken")
    
    print("\n   ✅ Integration test: COMPLETE FLOW SUCCESSFUL!")
    
except Exception as e:
    print(f"❌ Integration test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Final Summary
print("\n" + "="*70)
print("✅✅✅ PHASE 4 COMPLETE - ALL MODULES WORKING! ✅✅✅")
print("="*70)

print("\n📊 Phase 4 Summary:")
print("   ✅ context/memory_store.py - Persistent storage")
print("   ✅ context/state_tracker.py - State machine")
print("   ✅ context/context_manager.py - Context orchestrator")
print("   ✅ transaction/payment_processor.py - Payment logic")
print("   ✅ transaction/booking_handler.py - Booking validation")
print("   ✅ transaction/transaction_manager.py - Transaction orchestrator")
print("   ✅ qa/qa_knowledge.py - Knowledge base")
print("   ✅ qa/qa_retriever.py - Similarity retrieval")
print("   ✅ qa/qa_manager.py - QA orchestrator")

print("\n🎉 Phase 4 Complete!")
print("   📦 9 new modules created")
print("   🧪 All tests passing")
print("   🔄 Full booking flow working")
print("   💾 Context persistence working")
print("   💬 QA system functional")

print("\n" + "="*70)
print("🚀 Ready for Phase 5: FINAL INTEGRATION (Core + Main)!")
print("="*70 + "\n")