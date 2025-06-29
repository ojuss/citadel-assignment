from typing import Dict


class AlgorithmMonitor:
    """Monitor algorithm performance and user satisfaction metrics."""
    
    def __init__(self):
        self.metrics = {
            'profile_discovery': {
                'recommendations_served': 0,
                'mutual_likes': 0,
                'user_engagement_time': [],
                'algorithm_latency': []
            },
            'group_dining': {
                'groups_formed': 0,
                'satisfaction_ratings': [],
                'rebooking_rates': [],
                'algorithm_latency': []
            }
        }
    
    def log_profile_recommendation(self, latency_ms: float, user_engaged: bool, mutual_like: bool = False):
        """Log profile discovery metrics."""
        self.metrics['profile_discovery']['recommendations_served'] += 1
        self.metrics['profile_discovery']['algorithm_latency'].append(latency_ms)
        
        if mutual_like:
            self.metrics['profile_discovery']['mutual_likes'] += 1
    
    def log_group_formation(self, latency_ms: float, group_size: int, satisfaction_rating: float = None):
        """Log group dining metrics."""
        self.metrics['group_dining']['groups_formed'] += 1
        self.metrics['group_dining']['algorithm_latency'].append(latency_ms)
        
        if satisfaction_rating:
            self.metrics['group_dining']['satisfaction_ratings'].append(satisfaction_rating)
    
    def get_performance_summary(self) -> Dict:
        """Get current performance summary."""
        profile_metrics = self.metrics['profile_discovery']
        group_metrics = self.metrics['group_dining']
        
        return {
            'profile_discovery': {
                'total_recommendations': profile_metrics['recommendations_served'],
                'mutual_like_rate': (profile_metrics['mutual_likes'] / 
                                   max(profile_metrics['recommendations_served'], 1)) * 100,
                'avg_latency_ms': sum(profile_metrics['algorithm_latency']) / 
                                max(len(profile_metrics['algorithm_latency']), 1)
            },
            'group_dining': {
                'total_groups': group_metrics['groups_formed'],
                'avg_satisfaction': sum(group_metrics['satisfaction_ratings']) / 
                                 max(len(group_metrics['satisfaction_ratings']), 1),
                'avg_latency_ms': sum(group_metrics['algorithm_latency']) / 
                                max(len(group_metrics['algorithm_latency']), 1)
            }
        }
