import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from src.database import Database
from src.models.lstm_model import LottoLSTM
from src.models.xgboost_model import XGBoostPredictor
from src.models.prophet_model import ProphetForecaster
from src.models.ensemble import EnsemblePredictor
from src.analysis.bayesian_mcmc import BayesianMCMC
from src.analysis.time_series import JackpotTimeSeries
from src.analysis.rl_agent import RLBettingAgent
from src.analysis.jackpot_analyzer import JackpotAnalyzer
from src.config import Config
import joblib

def prepare_lstm_data(draws_df, seq_len=30):
    all_nums = []
    for nums in draws_df['numbers']:
        all_nums.extend(nums)
    arr = np.array(all_nums).reshape(-1, 1)
    minv, maxv = arr.min(), arr.max()
    scaled = (arr - minv) / (maxv - minv)
    X, y = [], []
    for i in range(seq_len, len(scaled)-1):
        X.append(scaled[i-seq_len:i, 0])
        y.append(scaled[i, 0])
    return np.array(X), np.array(y), minv, maxv

def train_all():
    db = Database()
    for game in ["Lotto", "Lotto Plus 1", "Lotto Plus 2", "Powerball"]:
        print(f"\n=== Training models for {game} ===")
        draws = db.get_historical_draws(game, 500)
        if len(draws) < 50:
            print("  Insufficient data")
            continue
        max_num = Config.GAME_PARAMS[game]["main_max"]
        # LSTM
        print("  Training LSTM...")
        X, y, minv, maxv = prepare_lstm_data(draws, Config.SEQUENCE_LENGTH)
        if len(X) > 0:
            X = X.reshape((X.shape[0], X.shape[1], 1))
            lstm = LottoLSTM(Config.SEQUENCE_LENGTH, 1)
            lstm.build_model()
            lstm.train(X, y, epochs=10, batch_size=32)  # small for demo
            lstm.save(f"models/{game}_lstm.h5")
            joblib.dump({'min':minv, 'max':maxv}, f"models/{game}_lstm_scaler.pkl")
        # XGBoost
        print("  Training XGBoost...")
        xgb = XGBoostPredictor(game, max_num)
        xgb.train(draws)
        xgb.save(f"models/{game}_xgboost.json")
        # Prophet
        print("  Training Prophet...")
        prophet = ProphetForecaster(game)
        prophet.fit(draws)
        prophet.save(f"models/{game}_prophet.pkl")
        # Bayesian
        print("  Sampling Bayesian MCMC...")
        bayes = BayesianMCMC(game, max_num)
        bayes.build_model(draws)
        bayes.sample_posterior(draws=500, tune=250)
        joblib.dump(bayes.trace, f"models/{game}_bayesian_trace.pkl")
        # Time series (jackpot)
        print("  Fitting SARIMA/GARCH...")
        ts = JackpotTimeSeries(game)
        jackpots = ts.prepare_data(draws)
        if len(jackpots) > 10:
            ts.fit_sarima(jackpots)
            ts.fit_garch(jackpots)
            joblib.dump(ts, f"models/{game}_timeseries.pkl")
        # RL
        print("  Training RL agent...")
        rl = RLBettingAgent(Config.GAME_PARAMS[game])
        rl.train(total_timesteps=20000)
        rl.model.save(f"models/{game}_rl_agent.zip")
        print(f"  ✓ All models saved for {game}")

if __name__ == "__main__":
    train_all()
