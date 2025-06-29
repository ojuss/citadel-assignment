import time
import random

from algorithms.profile_discovery import ProfileDiscoveryEngine
from algorithms.group_dining import GroupDiningMatcher
from models.user_profile import UserProfile


def create_performance_test_users(count: int = 1000) -> list:
    """Create users for performance testing."""
    users = []
    interests_pool = [
        "photography", "cooking", "hiking", "reading", "music", "traveling",
        "gaming", "sports", "art", "technology", "movies", "dancing"
    ]
    
    for i in range(count):
        user = UserProfile(
            user_id=f"user_{i}",
            age=random.randint(20, 28),
            gender=random.choice(["male", "female"]),
            city="Delhi",
            university=random.choice(["DU", "IIT", "JNU"]),
            degree=random.choice(["CS", "Business", "Engineering"]),
            graduation_year=random.randint(2024, 2027),
            dietary_restrictions=random.choice(["none", "vegetarian"]),
            budget_range=random.choice(["500-800", "800-1200"]),
            languages=["English", "Hindi"],
            alcohol=random.choice([True, False]),
            relationship_status=random.choice(["single", "in a relationship"]),
            interests=random.sample(interests_pool, 4),
            bio=f"Bio {i}",
        )
        users.append(user)
    
    return users


def test_profile_discovery_performance():
    """Test Profile Discovery performance."""
    print("Testing Profile Discovery performance...")
    
    users = create_performance_test_users(1000)
    engine = ProfileDiscoveryEngine()
    
    for user in users:
        engine.add_user(user)
    
    start_time = time.time()
    recommendation_count = 100
    
    for _ in range(recommendation_count):
        test_user = random.choice(users)
        recommendation = engine.select_next_profile(test_user.user_id)
    
    total_time = time.time() - start_time
    average_time_per_recommendation = (total_time / recommendation_count) * 1000  # ms
    
    print(f"Profile Discovery: {average_time_per_recommendation:.2f}ms per recommendation")
    return average_time_per_recommendation


def test_group_dining_performance():
    """Test Group Dining performance."""
    print("Testing Group Dining performance...")
    
    users = create_performance_test_users(1000)
    matcher = GroupDiningMatcher()
    
    for user in users:
        matcher.add_user(user)
    
    start_time = time.time()
    participating_users = random.sample(users, 100)
    groups = matcher.form_dining_groups(participating_users)
    total_time = (time.time() - start_time) * 1000  # ms
    
    print(f"Group Dining: {total_time:.2f}ms for 100 users, formed {len(groups)} groups")
    return total_time


def run_performance_tests():
    """Run performance tests for both algorithms."""
    print("=== Performance Test ===")
    
    profile_time = test_profile_discovery_performance()
    group_time = test_group_dining_performance()
    
    print(f"\nPerformance Summary:")
    print(f"- Profile Discovery: {profile_time:.2f}ms per recommendation")
    print(f"- Group Dining: {group_time:.2f}ms for 100 users")
    
    return {
        'profile_discovery_ms': profile_time,
        'group_dining_ms': group_time
    }


if __name__ == "__main__":
    run_performance_tests()
