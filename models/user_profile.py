from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class UserProfile:
    """Represents a user profile with personal, academic, and preference data."""
    
    user_id: str
    
    # Demographics
    age: int
    gender: str
    city: str
    university: str
    degree: str
    graduation_year: int
    
    # Preferences
    dietary_restrictions: str  # "none", "vegetarian", "vegan"
    budget_range: str  # "500-800", "800-1200", "1200+"
    languages: List[str]
    alcohol: bool
    relationship_status: str
    
    # Profile content
    interests: List[str]
    bio: str
    
    # Behavioral data
    liked_profiles: List[str] = None
    disliked_profiles: List[str] = None
    interaction_history: Dict = None
    
    def __post_init__(self):
        """Initialize empty lists and dictionaries if not provided."""
        if self.liked_profiles is None:
            self.liked_profiles = []
        if self.disliked_profiles is None:
            self.disliked_profiles = []
        if self.interaction_history is None:
            self.interaction_history = {}
