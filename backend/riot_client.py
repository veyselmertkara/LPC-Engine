import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv
import time
from tenacity import retry, stop_after_attempt, wait_exponential
from counter_data import COUNTER_DATABASE

# Load environment variables
load_dotenv()

class RiotAPIClient:
    """
    Real Riot Games API Client
    Fetches live player data, champion mastery, and match statistics
    """
    
    def __init__(self):
        self.api_key = os.getenv('RIOT_API_KEY')
        if not self.api_key:
            raise ValueError("RIOT_API_KEY not found in .env file!")
        
        self.headers = {
            'X-Riot-Token': self.api_key
        }
        
        # Region routing values
        self.region_routes = {
            'tr1': {'platform': 'tr1', 'regional': 'europe'},
            'euw1': {'platform': 'euw1', 'regional': 'europe'},
            'eun1': {'platform': 'eun1', 'regional': 'europe'},
            'na1': {'platform': 'na1', 'regional': 'americas'},
            'br1': {'platform': 'br1', 'regional': 'americas'},
            'la1': {'platform': 'la1', 'regional': 'americas'},
            'la2': {'platform': 'la2', 'regional': 'americas'},
            'kr': {'platform': 'kr', 'regional': 'asia'},
            'jp1': {'platform': 'jp1', 'regional': 'asia'},
        }
        
        # Data Dragon for champion data
        self.ddragon_version = "14.24.1"  # Update periodically
        self.champion_data = self._load_champion_data()
    
    def _load_champion_data(self) -> Dict:
        """Load champion data from Data Dragon"""
        try:
            url = f"https://ddragon.leagueoflegends.com/cdn/{self.ddragon_version}/data/en_US/champion.json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Create mapping: champion_id -> champion_name
                champion_map = {}
                for champ_name, champ_data in data['data'].items():
                    champion_map[champ_data['key']] = champ_data['name']
                    champion_map[champ_data['name'].lower()] = champ_data['name']
                return champion_map
            return {}
        except Exception as e:
            print(f"Failed to load champion data: {e}")
            return {}
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _make_request(self, url: str) -> Optional[Dict]:
        """Make API request with retry logic"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limited
                retry_after = int(response.headers.get('Retry-After', 5))
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                raise Exception("Rate limited, retrying...")
            elif response.status_code == 404:
                print(f"Resource not found: {url}")
                return None
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            raise
    
    def get_summoner_pool(self, name: str, tag: str, region: str = "tr1") -> List[Dict]:
        """
        Get summoner's champion pool using real Riot API
        
        Args:
            name: Summoner name (e.g., "Faker")
            tag: Tag line (e.g., "T1")
            region: Region code (e.g., "kr", "tr1", "euw1")
        
        Returns:
            List of champions with mastery data
        """
        region = region.lower()
        if region not in self.region_routes:
            print(f"Invalid region: {region}. Using tr1 as default.")
            region = 'tr1'
        
        routes = self.region_routes[region]
        
        # Step 1: Get PUUID from Riot ID
        account_url = f"https://{routes['regional']}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
        print(f"Fetching account: {name}#{tag}")
        
        account_data = self._make_request(account_url)
        if not account_data:
            print(f"Account not found: {name}#{tag}")
            return []
        
        puuid = account_data['puuid']
        print(f"Found PUUID: {puuid[:8]}...")
        
        # Step 2: Get Summoner data
        summoner_url = f"https://{routes['platform']}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        summoner_data = self._make_request(summoner_url)
        if not summoner_data:
            return []
        
        # Step 3: Get Champion Mastery
        mastery_url = f"https://{routes['platform']}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
        mastery_data = self._make_request(mastery_url)
        
        if not mastery_data:
            return []
        
        # Step 4: Build champion pool from mastery data only (fast!)
        # No match history needed - mastery points are sufficient indicator
        # Filter champions by mastery threshold
        # Using MASTERY POINTS as the primary indicator of champion proficiency
        MIN_MASTERY_THRESHOLD = 5000
        
        champion_pool = []
        
        for mastery in mastery_data:
            champ_id = str(mastery['championId'])
            champ_name = self.champion_data.get(champ_id, f"Champion_{champ_id}")
            mastery_points = mastery['championPoints']
            
            # FILTER: Only include champions with 5000+ mastery points
            if mastery_points >= MIN_MASTERY_THRESHOLD:
                champion_pool.append({
                    'championId': champ_name,
                    'championPoints': mastery_points,
                    'championLevel': mastery['championLevel']
                })
        
        print(f"Found {len(champion_pool)} champions in pool ({MIN_MASTERY_THRESHOLD}+ mastery each)")
        return champion_pool
    
    def get_global_counters(self, target_champion: str) -> Dict[str, float]:
        """
        Get global counter statistics for a champion
        
        Uses comprehensive counter database from counter_data.py
        For production, integrate with third-party APIs like U.GG or OP.GG
        """
        target = target_champion.lower()
        
        # Normalize target name and lookup in database
        for key in COUNTER_DATABASE.keys():
            if target in key or key in target:
                return COUNTER_DATABASE[key]
        
        # Generic counters if champion not in database
        return {
            'Jax': 0.51,
            'Malphite': 0.52,
            'Garen': 0.51,
            'Teemo': 0.50,
            'Darius': 0.51,
            'Renekton': 0.50,
            'Fiora': 0.51,
            'Camille': 0.50,
            'Sett': 0.50,
            'Mordekaiser': 0.51
        }


# Singleton instance
riot_client = RiotAPIClient()
