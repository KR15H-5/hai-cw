#!/usr/bin/env python3
"""
Complete Phase 2 Test Suite - Database Layer
Run from ROOT directory: python test_phase2_complete.py
"""

import os
import sys
import json

# Ensure we're in the right directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("🧪 PHASE 2: DATABASE LAYER - COMPLETE TEST SUITE")
print("="*70)

# Test 1: Movie Repository
print("\n" + "─"*70)
print("🎬 TEST 1: MOVIE REPOSITORY")
print("─"*70)

try:
    from database.movie_repository import MovieRepository
    
    repo = MovieRepository()
    
    # Test: Load movies
    movies = repo.get_all()
    assert len(movies) == 3, f"Expected 3 movies, got {len(movies)}"
    print(f"   ✅ Loaded {len(movies)} movies")
    
    # Test: Get single movie
    joker = repo.get('joker2')
    assert joker is not None, "Joker 2 not found"
    assert joker['title'] == 'Joker: Folie a Deux'
    print(f"   ✅ get('joker2'): {joker['title']}")
    
    # Test: Get all movies
    all_movies = repo.get_all()
    assert 'joker2' in all_movies
    assert 'dune2' in all_movies
    assert 'paddington3' in all_movies
    print(f"   ✅ get_all(): {list(all_movies.keys())}")
    
    # Test: Search movies
    results = repo.search('dune')
    assert len(results) > 0, "Search for 'dune' found nothing"
    print(f"   ✅ search('dune'): Found {len(results)} result(s)")
    
    results = repo.search('sci-fi')
    assert len(results) > 0, "Search for 'sci-fi' found nothing"
    print(f"   ✅ search('sci-fi'): Found {len(results)} result(s)")
    
    results = repo.search('Zendaya')
    assert len(results) > 0, "Search for 'Zendaya' found nothing"
    print(f"   ✅ search('Zendaya'): Found {len(results)} result(s)")
    
    # Test: Get by genre
    thriller_movies = repo.get_by_genre('thriller')
    assert len(thriller_movies) > 0
    print(f"   ✅ get_by_genre('thriller'): {len(thriller_movies)} movie(s)")
    
    family_movies = repo.get_by_genre('family')
    assert len(family_movies) > 0
    print(f"   ✅ get_by_genre('family'): {len(family_movies)} movie(s)")
    
    # Test: Get by rating
    pg_movies = repo.get_by_rating('PG')
    assert len(pg_movies) > 0
    print(f"   ✅ get_by_rating('PG'): {len(pg_movies)} movie(s)")
    
    # Test: Add movie (then remove it)
    test_movie = {
        'title': 'Test Movie',
        'genre': 'test',
        'rating': 'PG',
        'duration': '90 mins',
        'description': 'A test movie',
        'director': 'Test Director',
        'cast': ['Actor 1', 'Actor 2'],
        'times': ['10:00', '14:00'],
        'price': 10.00,
        'release_year': 2024
    }
    repo.add('test_movie', test_movie)
    added = repo.get('test_movie')
    assert added is not None
    print(f"   ✅ add('test_movie'): Movie added successfully")
    
    # Test: Update movie
    repo.update('test_movie', {'price': 15.00})
    updated = repo.get('test_movie')
    assert updated['price'] == 15.00
    print(f"   ✅ update('test_movie'): Price updated to £15.00")
    
    # Test: Delete movie (cleanup)
    repo.delete('test_movie')
    deleted = repo.get('test_movie')
    assert deleted is None
    print(f"   ✅ delete('test_movie'): Movie removed successfully")
    
    print("✅ MovieRepository: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ MovieRepository FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Booking Repository
print("\n" + "─"*70)
print("🎟️  TEST 2: BOOKING REPOSITORY")
print("─"*70)

try:
    from database.booking_repository import BookingRepository
    from utils.helpers import Helper
    
    repo = BookingRepository()
    
    # Test: Initial state
    initial_count = len(repo.get_all())
    print(f"   ✅ Initial bookings: {initial_count}")
    
    # Test: Add booking
    test_booking = {
        'reference': 'BK12345',
        'user_id': 'test_user',
        'user_name': 'Test User',
        'movie_key': 'joker2',
        'movie_title': 'Joker: Folie a Deux',
        'time': '14:00',
        'tickets': 2,
        'seats': [['A', 1], ['A', 2]],
        'total': 25.00
    }
    
    booking_id = repo.add(test_booking)
    assert booking_id > 0
    print(f"   ✅ add(): Booking created with ID {booking_id}")
    
    # Test: Get all bookings
    all_bookings = repo.get_all()
    assert len(all_bookings) == initial_count + 1
    print(f"   ✅ get_all(): {len(all_bookings)} total booking(s)")
    
    # Test: Get by user
    user_bookings = repo.get_by_user('test_user')
    assert len(user_bookings) > 0
    print(f"   ✅ get_by_user('test_user'): {len(user_bookings)} booking(s)")
    
    # Test: Get by reference
    found_booking = repo.get_by_reference('BK12345')
    assert found_booking is not None
    assert found_booking['user_name'] == 'Test User'
    print(f"   ✅ get_by_reference('BK12345'): Found booking")
    
    # Test: Get taken seats
    taken_seats = repo.get_taken_seats('joker2', '14:00')
    assert len(taken_seats) > 0
    assert ('A', 1) in taken_seats
    assert ('A', 2) in taken_seats
    print(f"   ✅ get_taken_seats('joker2', '14:00'): {len(taken_seats)} seat(s)")
    
    # Test: Get by movie
    movie_bookings = repo.get_by_movie('joker2')
    assert len(movie_bookings) > 0
    print(f"   ✅ get_by_movie('joker2'): {len(movie_bookings)} booking(s)")
    
    # Test: Add another booking (different seats)
    test_booking2 = {
        'reference': 'BK67890',
        'user_id': 'test_user',
        'user_name': 'Test User',
        'movie_key': 'dune2',
        'movie_title': 'Dune: Part Two',
        'time': '16:30',
        'tickets': 3,
        'seats': [['B', 5], ['B', 6], ['B', 7]],
        'total': 37.50
    }
    
    booking_id2 = repo.add(test_booking2)
    assert booking_id2 > booking_id
    print(f"   ✅ add(): Second booking created with ID {booking_id2}")
    
    # Verify taken seats updated
    taken_dune = repo.get_taken_seats('dune2', '16:30')
    assert ('B', 5) in taken_dune
    print(f"   ✅ Taken seats cache updated correctly")
    
    print("✅ BookingRepository: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ BookingRepository FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Database Manager
print("\n" + "─"*70)
print("💾 TEST 3: DATABASE MANAGER")
print("─"*70)

try:
    from database import DatabaseManager
    
    db = DatabaseManager()
    
    # Test: Get movie operations
    movie = db.get_movie('paddington3')
    assert movie is not None
    assert movie['title'] == 'Paddington in Peru'
    print(f"   ✅ get_movie('paddington3'): {movie['title']}")
    
    # Test: Get all movies
    all_movies = db.get_all_movies()
    assert len(all_movies) >= 3
    print(f"   ✅ get_all_movies(): {len(all_movies)} movies")
    
    # Test: Search movies
    results = db.search_movies('family')
    assert len(results) > 0
    print(f"   ✅ search_movies('family'): {len(results)} result(s)")
    
    # Test: Get user bookings
    user_bookings = db.get_user_bookings('test_user')
    assert len(user_bookings) >= 2  # We added 2 test bookings
    print(f"   ✅ get_user_bookings('test_user'): {len(user_bookings)} booking(s)")
    
    # Test: Get booking by reference
    booking = db.get_booking_by_reference('BK12345')
    assert booking is not None
    print(f"   ✅ get_booking_by_reference('BK12345'): Found")
    
    # Test: Get taken seats
    taken = db.get_taken_seats('joker2', '14:00')
    assert len(taken) > 0
    print(f"   ✅ get_taken_seats('joker2', '14:00'): {len(taken)} seat(s)")
    
    # Test: Check if seat is taken
    is_taken = db.is_seat_taken('joker2', '14:00', ('A', 1))
    assert is_taken == True
    print(f"   ✅ is_seat_taken('joker2', '14:00', ('A', 1)): {is_taken}")
    
    is_not_taken = db.is_seat_taken('joker2', '14:00', ('E', 10))
    assert is_not_taken == False
    print(f"   ✅ is_seat_taken('joker2', '14:00', ('E', 10)): {is_not_taken}")
    
    # Test: Get all bookings
    all_bookings = db.get_all_bookings()
    assert len(all_bookings) >= 2
    print(f"   ✅ get_all_bookings(): {len(all_bookings)} booking(s)")
    
    print("✅ DatabaseManager: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ DatabaseManager FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Integration Test
print("\n" + "─"*70)
print("🔗 TEST 4: INTEGRATION TEST")
print("─"*70)

try:
    from database import DatabaseManager
    
    db = DatabaseManager()
    
    # Scenario: User searches for a movie, checks seats, makes booking
    print("\n   📖 Scenario: Complete booking flow")
    
    # Step 1: Search for movie
    results = db.search_movies('thriller')
    assert len(results) > 0
    movie_key, movie = results[0]
    print(f"   1️⃣  Searched for 'thriller': Found {movie['title']}")
    
    # Step 2: Check available seats
    taken = db.get_taken_seats(movie_key, movie['times'][0])
    print(f"   2️⃣  Checked seats for {movie['times'][0]}: {len(taken)} taken")
    
    # Step 3: Select available seats
    all_seats = [(r, n) for r in ['A', 'B', 'C', 'D', 'E'] for n in range(1, 11)]
    available = [s for s in all_seats if s not in taken]
    selected_seats = available[:2]  # Book first 2 available
    print(f"   3️⃣  Selected seats: {selected_seats}")
    
    # Step 4: Create booking
    new_booking = {
        'reference': Helper.generate_reference(),
        'user_id': 'integration_test_user',
        'user_name': 'Integration Test',
        'movie_key': movie_key,
        'movie_title': movie['title'],
        'time': movie['times'][0],
        'tickets': 2,
        'seats': [[s[0], s[1]] for s in selected_seats],
        'total': movie['price'] * 2
    }
    
    booking_id = db.add_booking(new_booking)
    print(f"   4️⃣  Created booking: {new_booking['reference']}")
    
    # Step 5: Verify booking exists
    found = db.get_booking_by_reference(new_booking['reference'])
    assert found is not None
    print(f"   5️⃣  Verified booking exists: ✅")
    
    # Step 6: Verify seats are now taken
    for seat in selected_seats:
        is_taken = db.is_seat_taken(movie_key, movie['times'][0], seat)
        assert is_taken == True
    print(f"   6️⃣  Verified seats are marked as taken: ✅")
    
    print("\n   ✅ Integration test: COMPLETE BOOKING FLOW WORKS!")
    
except Exception as e:
    print(f"❌ Integration test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Data Persistence Test
print("\n" + "─"*70)
print("💾 TEST 5: DATA PERSISTENCE")
print("─"*70)

try:
    from database import DatabaseManager
    import config
    
    # Test: Check if data files exist
    assert os.path.exists(config.MOVIES_FILE), "movies.json not found"
    print(f"   ✅ movies.json exists")
    
    assert os.path.exists(config.BOOKINGS_FILE), "bookings.json not found"
    print(f"   ✅ bookings.json exists")
    
    # Test: Verify data was written
    with open(config.MOVIES_FILE, 'r') as f:
        movies_data = json.load(f)
        assert len(movies_data) >= 3
        print(f"   ✅ movies.json contains {len(movies_data)} movies")
    
    with open(config.BOOKINGS_FILE, 'r') as f:
        bookings_data = json.load(f)
        assert len(bookings_data) >= 3  # We added 3 test bookings
        print(f"   ✅ bookings.json contains {len(bookings_data)} bookings")
    
    # Test: Reload from disk
    db2 = DatabaseManager()
    movies_reloaded = db2.get_all_movies()
    bookings_reloaded = db2.get_all_bookings()
    
    assert len(movies_reloaded) == len(movies_data)
    assert len(bookings_reloaded) == len(bookings_data)
    print(f"   ✅ Data successfully reloaded from disk")
    
    print("✅ Data Persistence: ALL TESTS PASSED")
    
except Exception as e:
    print(f"❌ Data Persistence FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Final Summary
print("\n" + "="*70)
print("✅✅✅ PHASE 2 COMPLETE - ALL DATABASE TESTS PASSED! ✅✅✅")
print("="*70)

print("\n📊 Database Statistics:")
db = DatabaseManager()
print(f"   🎬 Total Movies: {len(db.get_all_movies())}")
print(f"   🎟️  Total Bookings: {len(db.get_all_bookings())}")

# Count taken seats
total_taken = 0
for movie_key in db.get_all_movies().keys():
    movie = db.get_movie(movie_key)
    for showtime in movie['times']:
        taken = db.get_taken_seats(movie_key, showtime)
        total_taken += len(taken)
print(f"   💺 Total Seats Booked: {total_taken}")

print("\n🎉 Database Layer is working perfectly!")
print("="*70)
print("\n📦 Phase 2 Summary:")
print("   ✅ database/movie_repository.py - Movie CRUD operations")
print("   ✅ database/booking_repository.py - Booking CRUD operations")
print("   ✅ database/db_manager.py - Database orchestrator")
print("   ✅ Data persistence working")
print("   ✅ Integration flow working")
print("\n🚀 Ready for Phase 3: Intent Classification & NLG!")
print("="*70 + "\n")