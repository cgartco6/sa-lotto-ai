import xgboost as xgb
import numpy as np
import pandas as pd
import joblib

class XGBoostPredictor:
    def __init__(self, game: str, max_number: int):
        self.game = game
        self.max_number = max_number
        self.model = None
        
    def prepare_features(self, draws_df: pd.DataFrame):
        X, y = [], []
        for i in range(6, len(draws_df)):
            features = []
            for j in range(i-6, i):
                features.extend(draws_df.iloc[j]['numbers'])
            X.append(features)
            y.extend(draws_df.iloc[i]['numbers'])
        return np.array(X), np.array(y)
    
    def train(self, draws_df: pd.DataFrame):
        X, y = self.prepare_features(draws_df)
        if len(X) == 0:
            return None
        self.model = xgb.XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1)
        self.model.fit(X, y)
        return self.model
    
    def predict_next(self, last_six_draws: list) -> list:
        if self.model is None:
            return []
        features = np.array(last_six_draws).flatten().reshape(1, -1)
        pred = self.model.predict(features)
        pred = np.clip(np.round(pred).astype(int), 1, self.max_number)
        return sorted(set(pred))[:6]
    
    def save(self, path):
        joblib.dump(self.model, path)
    
    def load(self, path):
        self.model = joblib.load(path)
