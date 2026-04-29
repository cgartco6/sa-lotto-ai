import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from typing import Dict, List

class JackpotAnalyzer:
    def __init__(self, game: str):
        self.game = game
        self.model_lr = None
        self.model_rf = None
        self.hw_fit = None
        
    def prepare_jackpot_series(self, draws_df: pd.DataFrame) -> pd.Series:
        df = draws_df.sort_values('draw_date')
        series = df['jackpot_amount'].copy()
        return series.fillna(method='ffill')
    
    def train_regression_models(self, jackpots: pd.Series):
        X = np.arange(len(jackpots)).reshape(-1, 1)
        y = jackpots.values
        self.model_lr = LinearRegression().fit(X, y)
        self.model_rf = RandomForestRegressor(n_estimators=50, random_state=42).fit(X, y)
        return self.model_lr, self.model_rf
    
    def train_holt_winters(self, jackpots: pd.Series, seasonal_periods: int = 52):
        model = ExponentialSmoothing(jackpots, trend='add', seasonal='add', seasonal_periods=seasonal_periods)
        self.hw_fit = model.fit()
        return self.hw_fit
    
    def predict_future_jackpots(self, steps: int = 10) -> Dict:
        if self.model_lr is None:
            raise ValueError("Train regression models first")
        last_idx = len(self.hw_fit.model.endog) if self.hw_fit else len(self.model_lr.predict(np.array([[0]])))
        future_idx = np.arange(last_idx, last_idx + steps).reshape(-1, 1)
        lr_pred = self.model_lr.predict(future_idx)
        rf_pred = self.model_rf.predict(future_idx)
        hw_pred = self.hw_fit.forecast(steps) if self.hw_fit else None
        if hw_pred is not None:
            ensemble = (lr_pred + rf_pred + hw_pred) / 3
        else:
            ensemble = (lr_pred + rf_pred) / 2
        return {
            "linear_regression": lr_pred,
            "random_forest": rf_pred,
            "holt_winters": hw_pred,
            "ensemble": ensemble,
            "steps": steps
        }
    
    def get_top6_jackpot_predictions(self, jackpots: pd.Series, future_steps: int = 6) -> List[float]:
        self.train_regression_models(jackpots)
        if len(jackpots) >= 52:
            self.train_holt_winters(jackpots)
        preds = self.predict_future_jackpots(steps=future_steps)
        return preds["ensemble"][:future_steps].tolist()
    
    def analyze_jackpot_history(self, draws_df: pd.DataFrame) -> Dict:
        series = self.prepare_jackpot_series(draws_df)
        diff = series.diff()
        rollovers = (diff > diff.median()).sum() if len(diff) > 0 else 0
        return {
            "average": series.mean(),
            "median": series.median(),
            "maximum": series.max(),
            "minimum": series.min(),
            "growth_rate": (series.iloc[-1] - series.iloc[0]) / len(series) if len(series) > 1 else 0,
            "rollover_count": rollovers,
            "last_jackpot": series.iloc[-1],
            "last_draw_date": draws_df.iloc[0]['draw_date'] if len(draws_df) else None
        }
    
    def detect_jackpot_anomaly(self, current_jackpot: float, historical: pd.Series, threshold_std: float = 2.0) -> bool:
        mean = historical.mean()
        std = historical.std()
        z_score = (current_jackpot - mean) / std if std > 0 else 0
        return abs(z_score) > threshold_std
