from pydantic import BaseModel
from typing import List, Optional

class ChampionRecommendationRequest(BaseModel):
    summoner_name: str
    tag_line: str # Added Tag Line (e.g. KR1)
    region: str = "na1" 
    target_champion: str 

class RecommendationDetail(BaseModel):
    global_wr: float
    mastery: int
    recent_wr: Optional[float] = None

class RecommendationResponse(BaseModel):
    champion_id: str
    champion_name: str 
    score: float
    details: RecommendationDetail

class GlobalCounterResponse(BaseModel):
    """Global counter pick (not filtered by user pool)"""
    champion_name: str
    win_rate: float
    in_user_pool: bool  # Whether user plays this champion

class RecommendationsList(BaseModel):
    target_champion: str
    global_counters: List[GlobalCounterResponse]  # All best counters globally
    user_pool_recommendations: List[RecommendationResponse]  # User's champions only
