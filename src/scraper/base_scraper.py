import requests
import pandas as pd
from typing import Dict, List, Optional

class BaseScraper:
    def __init__(self, game_name: str):
        self.game_name = game_name
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    def fetch_results(self, draw_id: Optional[int] = None) -> Optional[Dict]:
        raise NotImplementedError
    
    def parse_draw_data(self, raw_data: Dict) -> Dict:
        raise NotImplementedError
    
    def save_to_csv(self, results: List[Dict], filename: str):
        df = pd.DataFrame(results)
        df.to_csv(f"data/raw/{filename}.csv", index=False)
        return df
