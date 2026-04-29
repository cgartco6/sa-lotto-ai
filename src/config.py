import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, "data", "lottery.db"))
    
    LOTTO_API = "https://www.nationallottery.co.za/api/lotto-history"
    POWERBALL_API = "https://www.nationallottery.co.za/api/powerball-history"
    
    YOUR_NUMBERS = [9, 14, 17, 32, 39, 43]
    
    SEQUENCE_LENGTH = 30
    LSTM_EPOCHS = 50
    LSTM_BATCH_SIZE = 32
    
    TOP_N_POOL_SIZE = 13
    WHEEL_PICKED = 6
    WHEEL_GUARANTEE = 4
    
    MC_SIMULATIONS = 1_000_000
    
    GA_POPULATION_SIZE = 100
    GA_GENERATIONS = 50
    GA_MUTATION_RATE = 0.1
    
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    JACKPOT_THRESHOLDS = {
        "Lotto": 50_000_000,
        "Lotto Plus 1": 30_000_000,
        "Lotto Plus 2": 20_000_000,
        "Powerball": 80_000_000
    }
    
    GAME_PARAMS = {
        "Lotto": {"main_max": 58, "main_count": 6, "has_bonus": True},
        "Lotto Plus 1": {"main_max": 58, "main_count": 6, "has_bonus": True},
        "Lotto Plus 2": {"main_max": 58, "main_count": 6, "has_bonus": True},
        "Powerball": {"main_max": 50, "main_count": 5, "pb_max": 20, "has_bonus": False}
    }
