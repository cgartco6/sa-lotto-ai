import numpy as np
from src.analysis.frequency import FrequencyAnalyzer
from src.analysis.bayesian_mcmc import BayesianMCMC
import joblib

class EnsemblePredictor:
    def __init__(self, game: str, max_number: int):
        self.game = game
        self.max_number = max_number
        self.models = {}
        self.weights = {"lstm": 0.3, "xgboost": 0.25, "bayesian": 0.25, "freq": 0.2}
        
    def load_models(self, model_dir: str = "models/"):
        # LSTM loading would be here; for brevity we skip
        pass
    
    def predict_top13(self, draws_df, last_six_draws) -> tuple:
        freq = FrequencyAnalyzer.get_number_frequencies(draws_df, self.max_number)
        freq_top = FrequencyAnalyzer.get_top_n(freq, 13)
        # Placeholder: combine with other models if loaded
        top13 = freq_top[:13]
        top6 = top13[:6]
        return top13, top6
    
    def save(self, path):
        joblib.dump(self.weights, path)
    
    def load(self, path):
        self.weights = joblib.load(path)
