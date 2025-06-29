import random
import math
from typing import Optional, Dict

from models.user_profile import UserProfile


class ProfileDiscoveryEngine:
    """Algorithm for discovering and recommending compatible user profiles."""
    
    def __init__(self):
        self.user_profiles = {}
        self.similarity_cache = {}
        self.behavioral_models = {}
        
    def add_user(self, user: UserProfile):
        """Add a user to the system."""
        self.user_profiles[user.user_id] = user
        
    def calculate_academic_similarity(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate academic similarity score between two users (0-1)."""
        score = 0.0
        
        # Same university
        if user1.university == user2.university:
            score += 0.4
            
        # Same degree field
        if user1.degree == user2.degree:
            score += 0.3
            
        # Similar graduation year (within 1 year)
        year_difference = abs(user1.graduation_year - user2.graduation_year)
        if year_difference <= 1:
            score += 0.3 * (1 - year_difference / 2)
            
        return min(score, 1.0)
    
    def calculate_interest_compatibility(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate interest compatibility using Jaccard similarity with diversity bonus."""
        interests1 = set(user1.interests)
        interests2 = set(user2.interests)
        
        if not interests1 or not interests2:
            return 0.0
            
        intersection_count = len(interests1.intersection(interests2))
        union_count = len(interests1.union(interests2))
        
        # Base Jaccard similarity
        jaccard_score = intersection_count / union_count if union_count > 0 else 0
        
        # Apply diversity bonus - penalize identical interest sets
        diversity_multiplier = 1.0
        if intersection_count == len(interests1) == len(interests2):
            diversity_multiplier = 0.7  # Reduce score for identical interests
        elif intersection_count / min(len(interests1), len(interests2)) > 0.8:
            diversity_multiplier = 0.85  # Slight penalty for too much overlap
            
        return jaccard_score * diversity_multiplier
    
    def calculate_geographic_score(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate geographic proximity score."""
        if user1.city != user2.city:
            return 0.0
        
        # Same city gives base score
        return 0.8
    
    def calculate_behavioral_match(self, user: UserProfile, candidate: UserProfile, user_history: Dict) -> float:
        """Calculate behavioral compatibility based on user's like/dislike patterns."""
        if not user.liked_profiles:
            # Cold start - use demographic similarity
            return self.calculate_demographic_similarity(user, candidate)
        
        # Find users similar to candidate that the user has interacted with
        behavioral_score = 0.0
        similar_interaction_count = 0
        
        # Check recent likes
        for liked_user_id in user.liked_profiles[-10:]:
            if liked_user_id in self.user_profiles:
                liked_user = self.user_profiles[liked_user_id]
                similarity = self.calculate_profile_similarity(candidate, liked_user)
                if similarity > 0.3:  # Threshold for similarity
                    behavioral_score += similarity
                    similar_interaction_count += 1
        
        if similar_interaction_count > 0:
            return behavioral_score / similar_interaction_count
        
        # Check if candidate is similar to disliked profiles
        for disliked_user_id in user.disliked_profiles[-5:]:
            if disliked_user_id in self.user_profiles:
                disliked_user = self.user_profiles[disliked_user_id]
                similarity = self.calculate_profile_similarity(candidate, disliked_user)
                if similarity > 0.6:  # High similarity to disliked profile
                    return 0.1  # Low score
        
        return 0.5  # Neutral score
    
    def calculate_profile_similarity(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate overall profile similarity."""
        academic_score = self.calculate_academic_similarity(user1, user2)
        interest_score = self.calculate_interest_compatibility(user1, user2)
        
        # Weighted combination
        return academic_score * 0.4 + interest_score * 0.6
    
    def calculate_demographic_similarity(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate demographic similarity for cold start scenarios."""
        score = 0.0
        
        # Age similarity (within 2 years)
        age_difference = abs(user1.age - user2.age)
        if age_difference <= 2:
            score += 0.3 * (1 - age_difference / 5)
        
        # Academic similarity
        score += self.calculate_academic_similarity(user1, user2) * 0.5
        
        # Interest similarity
        score += self.calculate_interest_compatibility(user1, user2) * 0.2
        
        return min(score, 1.0)
    
    def calculate_diversity_bonus(self, user: UserProfile, candidate: UserProfile, user_history: Dict) -> float:
        """Calculate diversity bonus to encourage exploration."""
        if not user.liked_profiles:
            return 0.5
        
        # Check how different this candidate is from recent likes
        recent_likes = user.liked_profiles[-5:]
        diversity_scores = []
        
        for liked_user_id in recent_likes:
            if liked_user_id in self.user_profiles:
                liked_user = self.user_profiles[liked_user_id]
                similarity = self.calculate_profile_similarity(candidate, liked_user)
                diversity_scores.append(1 - similarity)  # Higher diversity = higher score
        
        if diversity_scores:
            return sum(diversity_scores) / len(diversity_scores)
        
        return 0.5
    
    def calculate_compatibility_score(self, user: UserProfile, candidate: UserProfile) -> float:
        """Main compatibility scoring function."""
        # Score weights
        ACADEMIC_WEIGHT = 0.20
        INTEREST_WEIGHT = 0.25
        GEOGRAPHIC_WEIGHT = 0.15
        BEHAVIORAL_WEIGHT = 0.30
        DIVERSITY_WEIGHT = 0.10
        
        academic_score = self.calculate_academic_similarity(user, candidate)
        interest_score = self.calculate_interest_compatibility(user, candidate)
        geographic_score = self.calculate_geographic_score(user, candidate)
        behavioral_score = self.calculate_behavioral_match(user, candidate, user.interaction_history)
        diversity_score = self.calculate_diversity_bonus(user, candidate, user.interaction_history)
        
        total_score = (
            academic_score * ACADEMIC_WEIGHT +
            interest_score * INTEREST_WEIGHT +
            geographic_score * GEOGRAPHIC_WEIGHT +
            behavioral_score * BEHAVIORAL_WEIGHT +
            diversity_score * DIVERSITY_WEIGHT
        )
        
        return total_score
    
    def get_exploration_rate(self, user: UserProfile) -> float:
        """Dynamic exploration rate based on user experience."""
        total_interactions = len(user.liked_profiles) + len(user.disliked_profiles)
        
        # Start with high exploration, decrease as user interacts more
        base_exploration_rate = 0.3
        decay_factor = 0.02
        minimum_exploration_rate = 0.05
        
        exploration_rate = base_exploration_rate * math.exp(-decay_factor * total_interactions)
        return max(exploration_rate, minimum_exploration_rate)
    
    def select_next_profile(self, user_id: str, max_candidates: int = 100) -> Optional[UserProfile]:
        """Select the next profile to show to the user."""
        if user_id not in self.user_profiles:
            return None
        
        user = self.user_profiles[user_id]
        
        # Get candidates (excluding self and already seen profiles)
        seen_profile_ids = set(user.liked_profiles + user.disliked_profiles + [user_id])
        candidates = [
            profile for profile_id, profile in self.user_profiles.items() 
            if profile_id not in seen_profile_ids
        ]
        
        if not candidates:
            return None
        
        # Limit candidates for performance
        if len(candidates) > max_candidates:
            candidates = random.sample(candidates, max_candidates)
        
        # Calculate scores for all candidates
        scored_candidates = []
        for candidate in candidates:
            score = self.calculate_compatibility_score(user, candidate)
            scored_candidates.append((candidate, score))
        
        # Sort by score (highest first)
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Apply exploration strategy (epsilon-greedy)
        exploration_rate = self.get_exploration_rate(user)
        
        if random.random() < exploration_rate:
            # Exploration: Select from top 20%
            top_candidate_count = max(1, len(scored_candidates) // 5)
            exploration_pool = scored_candidates[:top_candidate_count]
            return random.choice(exploration_pool)[0]
        else:
            # Exploitation: Select highest scoring candidate
            return scored_candidates[0][0]
    
    def update_user_feedback(self, user_id: str, candidate_id: str, liked: bool):
        """Update user preferences based on like/dislike feedback."""
        if user_id not in self.user_profiles:
            return
        
        user = self.user_profiles[user_id]
        
        if liked:
            user.liked_profiles.append(candidate_id)
        else:
            user.disliked_profiles.append(candidate_id)
        
        # Update behavioral model
        self.update_behavioral_model(user_id)
    
    def update_behavioral_model(self, user_id: str):
        """Update the behavioral model for a user."""
        # In production, this would update ML models
        user = self.user_profiles[user_id]
        user.interaction_history['last_updated'] = 'now'
