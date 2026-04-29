from .base_scraper import BaseScraper
from typing import Dict, Optional

class LottoScraper(BaseScraper):
    def __init__(self):
        super().__init__("Lotto")
        self.api_endpoint = "https://www.nationallottery.co.za/api/lotto-history"
    
    def fetch_results(self, draw_id: Optional[int] = None) -> Optional[Dict]:
        try:
            payload = {"drawId": draw_id} if draw_id else {}
            response = self.session.post(self.api_endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Lotto scraper error: {e}")
            return None
    
    def parse_draw_data(self, raw_data: Dict) -> Dict:
        nums_str = raw_data.get("winningNumbers", "")
        numbers = [int(x.strip()) for x in nums_str.split(",") if x.strip()]
        bonus = raw_data.get("bonusBall")
        if bonus is not None:
            bonus = int(bonus)
        return {
            "draw_id": raw_data.get("drawId"),
            "draw_date": raw_data.get("drawDate"),
            "numbers": numbers,
            "bonus_ball": bonus,
            "jackpot_amount": float(raw_data.get("jackpotAmount", 0))
        }
