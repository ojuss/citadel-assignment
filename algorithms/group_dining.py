import random
import math
import itertools
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
import numpy as np

from models.user_profile import UserProfile


class GroupDiningMatcher:
    """Algorithm for forming compatible dining groups based on user constraints and preferences."""
    
    def __init__(self):
        self.user_profiles = {}
        self.group_history = defaultdict(list)
        
    def add_user(self, user: UserProfile):
        """Add a user to the system."""
        self.user_profiles[user.user_id] = user
    
    def get_constraint_key(self, user: UserProfile) -> Tuple:
        """Generate constraint key for grouping compatible users."""
        return (
            user.dietary_restrictions,
            user.budget_range,
            user.city,
            tuple(sorted(user.languages))
        )
    
    def filter_compatible_users(self, available_users: List[UserProfile]) -> Dict[Tuple, List[UserProfile]]:
        """Group users by hard constraints (diet, budget, location, language)."""
        compatible_groups = defaultdict(list)
        
        for user in available_users:
            constraint_key = self.get_constraint_key(user)
            compatible_groups[constraint_key].append(user)
        
        # Filter groups with minimum viable size
        return {k: v for k, v in compatible_groups.items() if len(v) >= 6}
    
    def calculate_interest_diversity(self, group: List[UserProfile]) -> float:
        """Calculate interest diversity score using entropy."""
        all_interests = []
        for member in group:
            all_interests.extend(member.interests)
        
        if not all_interests:
            return 0.0
        
        # Calculate interest distribution
        interest_counts = Counter(all_interests)
        total_interest_mentions = len(all_interests)
        
        # Calculate entropy (diversity measure)
        entropy = 0.0
        for count in interest_counts.values():
            probability = count / total_interest_mentions
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        # Normalize entropy (max entropy for uniform distribution)
        max_possible_entropy = math.log2(len(interest_counts)) if len(interest_counts) > 1 else 1
        normalized_entropy = entropy / max_possible_entropy if max_possible_entropy > 0 else 0
        
        return normalized_entropy
    
    def calculate_conversation_potential(self, group: List[UserProfile]) -> float:
        """Calculate conversation potential based on shared interests and diversity."""
        # Count pairs with shared interests
        shared_interest_pairs = 0
        total_possible_pairs = len(group) * (len(group) - 1) / 2
        
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                user1_interests = set(group[i].interests)
                user2_interests = set(group[j].interests)
                
                shared_interests = len(user1_interests.intersection(user2_interests))
                if shared_interests >= 1:  # At least one shared interest
                    shared_interest_pairs += 1
        
        # Aim for 60-80% of pairs having shared interests
        optimal_shared_ratio = 0.7
        actual_shared_ratio = shared_interest_pairs / total_possible_pairs if total_possible_pairs > 0 else 0
        
        # Score based on how close to optimal ratio
        if actual_shared_ratio <= optimal_shared_ratio:
            return actual_shared_ratio / optimal_shared_ratio
        else:
            # Penalize too much similarity
            excess_similarity = (actual_shared_ratio - optimal_shared_ratio) / (1.0 - optimal_shared_ratio)
            return 1.0 - (excess_similarity * 0.3)
    
    def calculate_demographic_balance(self, group: List[UserProfile]) -> float:
        """Calculate demographic balance score."""
        if len(group) < 2:
            return 0.0
        
        balance_score = 0.0
        
        # Age diversity (prefer mix of ages, not all same age)
        ages = [user.age for user in group]
        age_standard_deviation = np.std(ages)
        age_balance = min(age_standard_deviation / 3.0, 1.0)  # Normalize by expected std
        balance_score += age_balance * 0.3
        
        # Gender balance
        genders = [user.gender for user in group]
        gender_counts = Counter(genders)
        gender_balance = 1.0 - abs(0.5 - min(gender_counts.values()) / len(group)) * 2
        balance_score += gender_balance * 0.3
        
        # University diversity
        universities = [user.university for user in group]
        unique_university_count = len(set(universities))
        university_balance = min(unique_university_count / 3.0, 1.0)  # Prefer 3+ different universities
        balance_score += university_balance * 0.2
        
        # Relationship status consideration
        relationship_statuses = [user.relationship_status for user in group]
        status_counts = Counter(relationship_statuses)
        # Prefer balanced mix of relationship statuses
        if len(status_counts) > 1:
            status_balance = 1.0 - (max(status_counts.values()) / len(group) - 1/len(status_counts))
        else:
            status_balance = 0.5
        balance_score += status_balance * 0.2
        
        return balance_score
    
    def calculate_social_compatibility(self, group: List[UserProfile]) -> float:
        """Calculate social compatibility based on personality indicators."""
        # Use alcohol preference as social style indicator
        alcohol_preferences = [user.alcohol for user in group]
        alcohol_positive_count = sum(alcohol_preferences)
        
        # Prefer mixed groups but not extreme mismatches
        alcohol_ratio = alcohol_positive_count / len(group)
        if 0.3 <= alcohol_ratio <= 0.7:
            alcohol_compatibility = 1.0
        else:
            alcohol_compatibility = 0.7
        
        # Relationship status compatibility
        single_count = sum(1 for user in group if user.relationship_status == "single")
        single_ratio = single_count / len(group)
        
        # Prefer groups that aren't all couples or all singles
        if 0.2 <= single_ratio <= 0.8:
            relationship_compatibility = 1.0
        else:
            relationship_compatibility = 0.8
        
        return (alcohol_compatibility + relationship_compatibility) / 2
    
    def calculate_group_score(self, group: List[UserProfile]) -> float:
        """Calculate overall group quality score."""
        # Score component weights
        DIVERSITY_WEIGHT = 0.4
        BALANCE_WEIGHT = 0.3
        SOCIAL_WEIGHT = 0.3
        
        diversity_score = self.calculate_interest_diversity(group)
        conversation_score = self.calculate_conversation_potential(group)
        balance_score = self.calculate_demographic_balance(group)
        social_score = self.calculate_social_compatibility(group)
        
        # Combine diversity and conversation for overall interest score
        interest_score = diversity_score * 0.6 + conversation_score * 0.4
        
        total_score = (
            interest_score * DIVERSITY_WEIGHT +
            balance_score * BALANCE_WEIGHT +
            social_score * SOCIAL_WEIGHT
        )
        
        return total_score
    
    def apply_fairness_boost(self, user: UserProfile, base_score: float) -> float:
        """Apply fairness boost for users who haven't had good experiences."""
        user_group_history = self.group_history.get(user.user_id, [])
        
        if len(user_group_history) == 0:
            return base_score  # New user, no boost needed
        
        # Users who haven't been in many groups get boost
        if len(user_group_history) < 3:
            fairness_boost = 0.15
        else:
            fairness_boost = 0.0
        
        return base_score + fairness_boost
    
    def select_non_overlapping_groups(self, scored_groups: List[Tuple[List[UserProfile], float]], 
                                    target_group_size: int = 6) -> List[List[UserProfile]]:
        """Select non-overlapping groups with highest scores."""
        # Sort groups by score (highest first)
        scored_groups.sort(key=lambda x: x[1], reverse=True)
        
        selected_groups = []
        used_user_ids = set()
        
        for group, score in scored_groups:
            # Check if any user in this group is already used
            group_user_ids = {user.user_id for user in group}
            
            if not group_user_ids.intersection(used_user_ids):
                # No overlap, add this group
                selected_groups.append(group)
                used_user_ids.update(group_user_ids)
        
        return selected_groups
    
    def form_dining_groups(self, available_users: List[UserProfile], 
                          target_group_size: int = 6) -> List[List[UserProfile]]:
        """Main function to form dining groups."""
        
        # Step 1: Filter by hard constraints
        compatible_groups = self.filter_compatible_users(available_users)
        
        all_possible_groups = []
        
        # Step 2: Generate and score groups within each constraint group
        for constraint_key, users in compatible_groups.items():
            if len(users) < target_group_size:
                continue
            
            # For large groups, use sampling to avoid combinatorial explosion
            if len(users) > 20:
                # Sample combinations rather than generating all
                sample_combinations = []
                sample_count = min(1000, len(users) * 10)  # Reasonable sample size
                for _ in range(sample_count):
                    if len(users) >= target_group_size:
                        sampled_group = random.sample(users, target_group_size)
                        sample_combinations.append(sampled_group)
                possible_groups = sample_combinations
            else:
                # Generate all combinations for smaller groups
                possible_groups = list(itertools.combinations(users, target_group_size))
            
            # Score each possible group
            for group in possible_groups:
                group_list = list(group)
                base_score = self.calculate_group_score(group_list)
                
                # Apply fairness adjustments
                fairness_adjusted_score = base_score
                for user in group_list:
                    individual_boost = self.apply_fairness_boost(user, 0) * 0.1  # Small individual boost
                    fairness_adjusted_score += individual_boost
                
                all_possible_groups.append((group_list, fairness_adjusted_score))
        
        # Step 3: Select non-overlapping groups with highest scores
        final_groups = self.select_non_overlapping_groups(all_possible_groups, target_group_size)
        
        # Step 4: Update group history
        for group in final_groups:
            for user in group:
                self.group_history[user.user_id].append({
                    'group_members': [u.user_id for u in group],
                    'timestamp': 'now'  # In practice, use actual timestamp
                })
        
        return final_groups
