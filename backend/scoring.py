import math
from typing import Optional

class ScoringEngine:
    def __init__(self, weights: dict = None):
        if weights is None:
            # Global WR is the dominant factor (80%)
            # Mastery is secondary (20%)
            # No recent performance tracking for speed
            self.weights = {'global': 0.80, 'mastery': 0.20}
        else:
            self.weights = weights

    def calculate_score(
        self,
        global_wr_vs_target: float,  # e.g., 0.53 representing 53%
        user_mastery_points: int    # e.g., 150000
    ) -> float:
        """
        Calculates a suitability score for a champion pick effectively counter-picking a target.
        Score is 0-100.
        
        OPTIMIZED LOGIC: Only uses Global WR (80%) and Mastery (20%)
        - Fast performance - no match history needed
        - Global WR is the PRIMARY factor
        - Mastery shows player proficiency
        """
        
        # 1. Global Advantage Score (0-100) - DOMINANT FACTOR
        # Baseline: 50% WR -> 50 points.
        # Scaling: Each 1% WR deviation is worth 5 points
        # 55% WR -> 50 + 5*5 = 75 points
        # 60% WR -> 50 + 10*5 = 100 points
        # 45% WR -> 50 - 5*5 = 25 points
        global_score = 50 + (global_wr_vs_target - 0.50) * 100 * 5
        global_score = max(0, min(100, global_score))

        # 2. Mastery Score (0-100) - SECONDARY FACTOR
        # Logarithmic scale.
        # 5k pts -> base comfort
        # 10k pts -> decent comfort
        # 100k pts -> high comfort
        # 1M pts -> mastery
        if user_mastery_points < 1000:
            mastery_score = 0
        else:
            # log10(1000) = 3. 
            # log10(1M) = 6.
            # Range of interest: 3.0 to 6.0
            log_mastery = math.log10(user_mastery_points)
            
            # Map 3.0->6.0 to roughly 20->100
            # 1k (3.0) -> 20 (base familiarity)
            # 10k (4.0) -> 46
            # 100k (5.0) -> 73
            # 1M (6.0) -> 100
            mastery_score = (log_mastery - 3) * 26.6 + 20
            mastery_score = max(0, min(100, mastery_score))

        # 3. Weighted Aggregate (Global WR is 80%, Mastery is 20%)
        final_score = (
            (global_score * self.weights['global']) +
            (mastery_score * self.weights['mastery'])
        )

        return round(final_score, 2)

    def generate_recommendations(self, target_champion_id: str, user_pool: list, global_stats: dict):
        """
        OPTIMIZED APPROACH: Filter global counters by user's champion pool
        
        Instead of scoring all user champions, we:
        1. Take the global counter list (sorted by win rate)
        2. Filter to only include champions the user plays
        3. Apply mastery as a secondary sort factor
        
        user_pool: List of dicts { 'champion_id': 'Jax', 'mastery': 200000 }
        global_stats: Dict of { 'champion_id': win_rate_vs_target }
        """
        
        # Create a lookup for user's champion pool
        user_champions = {champ['champion_id']: champ for champ in user_pool}
        
        recommendations = []
        
        # Sort global counters by win rate (descending)
        sorted_counters = sorted(global_stats.items(), key=lambda x: x[1], reverse=True)
        
        # Filter to only include champions the user plays
        for champion_name, global_wr in sorted_counters:
            if champion_name in user_champions:
                user_data = user_champions[champion_name]
                
                # Calculate score (heavily weighted towards global WR)
                score = self.calculate_score(
                    global_wr_vs_target=global_wr,
                    user_mastery_points=user_data.get('mastery', 0)
                )
                
                recommendations.append({
                    'champion_id': champion_name,
                    'score': score,
                    'details': {
                        'global_wr': global_wr,
                        'mastery': user_data.get('mastery', 0)
                    }
                })
        
        # Also include user champions not in global counter list (with default 50% WR)
        for champion_name, user_data in user_champions.items():
            if champion_name not in global_stats:
                score = self.calculate_score(
                    global_wr_vs_target=0.50,  # Neutral
                    user_mastery_points=user_data.get('mastery', 0)
                )
                
                recommendations.append({
                    'champion_id': champion_name,
                    'score': score,
                    'details': {
                        'global_wr': 0.50,
                        'mastery': user_data.get('mastery', 0)
                    }
                })
        
        # Sort by score descending (global WR is now the dominant factor)
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)

