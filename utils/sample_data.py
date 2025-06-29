import random
from typing import List

from models.user_profile import UserProfile


def create_sample_users(count: int = 50) -> List[UserProfile]:
    """Create sample users for testing algorithms."""
    sample_users = []
    
    # Sample data pools
    interests_pool = [
        "photography", "cooking", "hiking", "reading", "music", "traveling",
        "gaming", "sports", "art", "technology", "movies", "dancing",
        "yoga", "writing", "entrepreneurship", "volunteering"
    ]
    
    universities = ["Delhi University", "IIT Delhi", "JNU", "AIIMS", "DTU"]
    degrees = ["Computer Science", "Business", "Medicine", "Engineering", "Arts"]
    cities = ["Delhi", "Mumbai", "Bangalore"]
    
    for i in range(count):
        user = UserProfile(
            user_id=f"user_{i}",
            age=random.randint(20, 28),
            gender=random.choice(["male", "female", "non-binary"]),
            city=random.choice(cities),
            university=random.choice(universities),
            degree=random.choice(degrees),
            graduation_year=random.randint(2024, 2027),
            
            dietary_restrictions=random.choice(["none", "vegetarian", "vegan"]),
            budget_range=random.choice(["500-800", "800-1200", "1200+"]),
            languages=random.sample(["English", "Hindi", "Punjabi", "Tamil"], 
                                  random.randint(1, 3)),
            alcohol=random.choice([True, False]),
            relationship_status=random.choice(["single", "in a relationship", "not looking"]),
            
            interests=random.sample(interests_pool, random.randint(3, 5)),
            bio=f"Sample bio for user {i}",
        )
        sample_users.append(user)
    
    return sample_users
