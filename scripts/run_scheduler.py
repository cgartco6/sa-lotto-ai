import schedule
import time
from src.scraper.run_scraper import scrape_all
from src.telegram.alerts import AlertManager
from scripts.train_models import train_all
from scripts.update_data import update_data
from src.analysis.jackpot_analyzer import JackpotAnalyzer
from src.database import Database

def job():
    print("Running scheduled tasks...")
    update_data()
    train_all()
    
    # Send jackpot prediction alerts
    db = Database()
    alert = AlertManager()
    for game in ["Lotto", "Lotto Plus 1", "Lotto Plus 2", "Powerball"]:
        draws = db.get_historical_draws(game, 100)
        if len(draws) > 10:
            ja = JackpotAnalyzer(game)
            series = ja.prepare_jackpot_series(draws)
            top6 = ja.get_top6_jackpot_predictions(series, future_steps=6)
            anomaly = ja.detect_jackpot_anomaly(series.iloc[-1], series[:-1])
            alert.send_jackpot_prediction_alert(game, top6, anomaly)
    
    AlertManager().check_jackpot_alerts()

schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    print("Scheduler started. Waiting for tasks...")
    while True:
        schedule.run_pending()
        time.sleep(60)
