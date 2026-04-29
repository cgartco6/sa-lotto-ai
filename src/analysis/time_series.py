import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from arch import arch_model
from typing import Tuple, Dict

class JackpotTimeSeries:
    def __init__(self, game: str):
        self.game = game
        self.sarima_fit = None
        self.garch_fit = None
        
    def prepare_data(self, draws_df: pd.DataFrame) -> pd.Series:
        jackpots = draws_df.sort_values('draw_date')['jackpot_amount']
        return jackpots.fillna(method='ffill')
    
    def fit_sarima(self, jackpots: pd.Series, order=(1,1,1), seasonal_order=(1,1,1,52)):
        model = SARIMAX(jackpots, order=order, seasonal_order=seasonal_order)
        self.sarima_fit = model.fit(disp=False)
        return self.sarima_fit
    
    def forecast_jackpot(self, steps: int = 10) -> np.ndarray:
        if self.sarima_fit is None:
            raise ValueError("Call fit_sarima first")
        return self.sarima_fit.forecast(steps=steps).values
    
    def fit_garch(self, jackpots: pd.Series, p=1, q=1):
        returns = jackpots.pct_change().dropna() * 100
        model = arch_model(returns, p=p, q=q, vol='Garch')
        self.garch_fit = model.fit(disp='off')
        return self.garch_fit
    
    def detect_jackpot_anomaly(self, current_jackpot: float, historical: pd.Series) -> Dict:
        mean = historical.mean()
        std = historical.std()
        z_score = (current_jackpot - mean) / std if std > 0 else 0
        return {
            'anomaly_score': abs(z_score),
            'is_ready_to_payout': abs(z_score) > 1.5,
            'z_score': z_score
        }
