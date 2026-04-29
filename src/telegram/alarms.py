from src.database import Database
from src.config import Config
from src.telegram.bot import TelegramBot
from src.analysis.jackpot_analyzer import JackpotAnalyzer

class AlertManager:
    def __init__(self):
        self.db = Database()
        self.bot = TelegramBot()
    
    def check_jackpot_alerts(self):
        for game, threshold in Config.JACKPOT_THRESHOLDS.items():
            draws = self.db.get_historical_draws(game, limit=1)
            if not draws.empty:
                latest = draws.iloc[0]['jackpot_amount']
                if latest >= threshold:
                    self.bot.sync_send(f"🚨 JACKPOT ALERT! {game} is R{latest:,.0f}")
    
    def send_jackpot_prediction_alert(self, game: str, top6: list, anomaly: bool):
        msg = f"💰 *{game} Jackpot Forecast*\nTop 6 predictions:\n"
        for i, v in enumerate(top6[:6], 1):
            msg += f"{i}. R{v:,.0f}\n"
        if anomaly:
            msg += "\n🚨 ANOMALY – likely payout soon!"
        self.bot.sync_send(msg)
