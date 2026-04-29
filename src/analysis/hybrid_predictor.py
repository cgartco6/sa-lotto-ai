import numpy as np
import pandas as pd   # <--- ADDED (was missing)
from src.analysis.frequency import FrequencyAnalyzer
from src.analysis.patterns import PatternAnalyzer
from src.analysis.pairs import PairAnalyzer
from src.analysis.bayesian_mcmc import BayesianMCMC
from src.analysis.time_series import JackpotTimeSeries
from src.analysis.rl_agent import RLBettingAgent
from src.analysis.jackpot_analyzer import JackpotAnalyzer
from src.config import Config

class HybridPredictor:
    def __init__(self, game: str, max_number: int):
        self.game = game
        self.max_number = max_number
        self.bayesian = BayesianMCMC(game, max_number)
        self.ts = JackpotTimeSeries(game)
        self.rl = RLBettingAgent(Config.GAME_PARAMS[game])
        self.jackpot_analyzer = JackpotAnalyzer(game)
        
    def analyze_all(self, draws_df):
        # Frequency
        freq = FrequencyAnalyzer.get_number_frequencies(draws_df, self.max_number)
        top_freq = FrequencyAnalyzer.get_top_n(freq, 13)
        # Pairs
        pairs = PairAnalyzer.get_frequent_pairs(draws_df, 10)
        # Sequences
        sequences = PatternAnalyzer.detect_sequences(draws_df, 3)
        # Bayesian
        self.bayesian.build_model(draws_df)
        self.bayesian.sample_posterior(draws=500, tune=250)
        bayes_top = self.bayesian.predict_top_n(13)
        # Jackpot analysis
        jackpot_res = self.predict_jackpots(draws_df, 6)
        # RL advice
        last_jackpot = draws_df.iloc[0]['jackpot_amount'] if len(draws_df) else 0
        bet_advice = self.rl.get_bet_advice(10000, last_jackpot, 0)
        # Combined top13
        combined_scores = {}
        for i, num in enumerate(top_freq): combined_scores[num] = (13-i)*0.4
        for i, num in enumerate(bayes_top): combined_scores[num] = combined_scores.get(num,0) + (13-i)*0.4
        for pair, count in pairs:
            for num in pair:
                combined_scores[num] = combined_scores.get(num,0) + count/100
        top13 = sorted(combined_scores, key=combined_scores.get, reverse=True)[:13]
        top6 = top13[:6]
        return {
            "top13": top13,
            "top6": top6,
            "jackpot_forecast": jackpot_res['future_predictions']['ensemble'],
            "jackpot_anomaly": jackpot_res['anomaly_detected'],
            "bet_advice": bet_advice,
            "frequent_pairs": pairs,
            "detected_sequences": sequences,
            "jackpot_top6": jackpot_res['top6_jackpot_predictions']
        }
    
    def predict_jackpots(self, draws_df: pd.DataFrame, future_steps: int = 6) -> dict:
        series = self.jackpot_analyzer.prepare_jackpot_series(draws_df)
        self.jackpot_analyzer.train_regression_models(series)
        if len(series) >= 52:
            self.jackpot_analyzer.train_holt_winters(series)
        preds = self.jackpot_analyzer.predict_future_jackpots(steps=future_steps)
        top6 = self.jackpot_analyzer.get_top6_jackpot_predictions(series, future_steps)
        history_stats = self.jackpot_analyzer.analyze_jackpot_history(draws_df)
        is_anomaly = self.jackpot_analyzer.detect_jackpot_anomaly(series.iloc[-1], series[:-1])
        return {
            "top6_jackpot_predictions": top6,
            "future_predictions": preds,
            "historical_stats": history_stats,
            "anomaly_detected": is_anomaly
        }
