from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Use Absolute Imports to avoid script issues
from models import ChampionRecommendationRequest, RecommendationsList, RecommendationResponse, RecommendationDetail, GlobalCounterResponse
from scoring import ScoringEngine
from riot_client import riot_client

app = FastAPI(title="LPC-Engine API", version="0.1.0")

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scorer = ScoringEngine()

@app.get("/")
def read_root():
    return {"message": "LPC-Engine Backend [Real Riot API] is Running", "status": "ready"}

@app.post("/recommend", response_model=RecommendationsList)
def get_recommendations(request: ChampionRecommendationRequest):
    """
    Uses Real Riot API for user pool and champion data.
    """
    print(f"Request received: {request.summoner_name} #{request.tag_line} vs {request.target_champion}")
    
    # 1. Fetch User Data (Real Riot API)
    user_pool_data = riot_client.get_summoner_pool(request.summoner_name, request.tag_line, request.region)
    
    # 2. Fetch Global Counters
    global_counters = riot_client.get_global_counters(request.target_champion)
    
    # 3. Prepare for Scorer
    user_pool_prepared = []
    
    if not user_pool_data:
        # If scraping failed, return empty or informative error? 
        # For UX, we might return a "Generic" set if 404, but better to warn.
        # But let's proceed with an empty pool -> Empty recommendations -> Frontend shows fallback.
        pass

    for champ in user_pool_data:
        # champ = { championId, championPoints, championLevel }
        user_pool_prepared.append({
            'champion_id': champ['championId'],
            'mastery': champ.get('championPoints', 0)
        })

    # 4. Prepare global counters list (top 10)
    user_champion_names = {champ['champion_id'] for champ in user_pool_prepared}
    
    global_counter_list = []
    sorted_counters = sorted(global_counters.items(), key=lambda x: x[1], reverse=True)
    
    for champion_name, win_rate in sorted_counters[:10]:  # Top 10 global counters
        global_counter_list.append(GlobalCounterResponse(
            champion_name=champion_name,
            win_rate=win_rate,
            in_user_pool=(champion_name in user_champion_names)
        ))

    # 5. Prepare user pool recommendations
    # ONLY include champions that are in the top 10 global counters AND in user's pool
    user_pool_list = []
    
    for champion_name, win_rate in sorted_counters[:10]:  # Top 10 global counters
        if champion_name in user_champion_names:  # Only if user plays this champion
            # Find user data for this champion
            user_data = next((c for c in user_pool_prepared if c['champion_id'] == champion_name), None)
            
            if user_data:
                # Calculate score (no recent_wr needed - faster!)
                score = scorer.calculate_score(
                    global_wr_vs_target=win_rate,
                    user_mastery_points=user_data.get('mastery', 0)
                )
                
                user_pool_list.append(RecommendationResponse(
                    champion_id=champion_name,
                    champion_name=champion_name,
                    score=score,
                    details=RecommendationDetail(
                        global_wr=win_rate,
                        mastery=user_data.get('mastery', 0),
                        recent_wr=None  # No longer tracked for performance
                    )
                ))
    
    # Sort user pool by score (descending)
    user_pool_list.sort(key=lambda x: x.score, reverse=True)

    return RecommendationsList(
        target_champion=request.target_champion,
        global_counters=global_counter_list,
        user_pool_recommendations=user_pool_list
    )


