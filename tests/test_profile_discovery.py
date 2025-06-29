import random
from collections import Counter

from algorithms.profile_discovery import ProfileDiscoveryEngine
from utils.sample_data import create_sample_users


def demo_profile_discovery():
    """Demonstrate the Profile Discovery Engine."""
    print("=== Profile Discovery Engine Demo ===")
    
    # Create engine and sample users
    engine = ProfileDiscoveryEngine()
    users = create_sample_users()
    
    # Add users to engine
    for user in users:
        engine.add_user(user)
    
    # Simulate user interactions
    test_user = users[0]
    print(f"Test user: {test_user.user_id} ({test_user.university}, {test_user.interests})")
    
    # Show 5 recommended profiles
    for i in range(5):
        recommended_profile = engine.select_next_profile(test_user.user_id)
        if recommended_profile:
            compatibility_score = engine.calculate_compatibility_score(test_user, recommended_profile)
            print(f"\nRecommendation {i+1}: {recommended_profile.user_id}")
            print(f"  University: {recommended_profile.university}, Interests: {recommended_profile.interests}")
            print(f"  Compatibility Score: {compatibility_score:.3f}")
            
            # Simulate user feedback (random for demo)
            user_liked = random.choice([True, False])
            engine.update_user_feedback(test_user.user_id, recommended_profile.user_id, user_liked)
            print(f"  User reaction: {'Liked' if user_liked else 'Disliked'}")


if __name__ == "__main__":
    demo_profile_discovery()
