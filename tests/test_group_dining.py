import random
from collections import Counter

from algorithms.group_dining import GroupDiningMatcher
from utils.sample_data import create_sample_users


def demo_group_dining():
    """Demonstrate the Group Dining Matcher."""
    print("=== Group Dining Matcher Demo ===")
    
    # Create matcher and sample users
    matcher = GroupDiningMatcher()
    users = create_sample_users()
    
    # Add users to matcher
    for user in users:
        matcher.add_user(user)
    
    # Filter users who want to participate (random subset)
    participating_users = random.sample(users, 25)  # 25 users want to dine
    
    print(f"Creating dining groups from {len(participating_users)} participants")
    
    # Form groups
    groups = matcher.form_dining_groups(participating_users)
    
    print(f"\nFormed {len(groups)} dining groups:")
    
    for i, group in enumerate(groups):
        print(f"\nGroup {i+1} ({len(group)} members):")
        
        # Show group composition
        dietary_restrictions = Counter(user.dietary_restrictions for user in group)
        budget_ranges = Counter(user.budget_range for user in group)
        universities = set(user.university for user in group)
        
        all_interests = []
        for user in group:
            all_interests.extend(user.interests)
        common_interests = Counter(all_interests)
        
        print(f"  Dietary: {dict(dietary_restrictions)}")
        print(f"  Budget: {dict(budget_ranges)}")
        print(f"  Universities: {universities}")
        print(f"  Top interests: {dict(common_interests.most_common(5))}")
        
        # Calculate and show group score
        group_quality_score = matcher.calculate_group_score(group)
        print(f"  Group Quality Score: {group_quality_score:.3f}")


if __name__ == "__main__":
    demo_group_dining()
