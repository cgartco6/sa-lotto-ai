from prophet import Prophet
import pandas as pd
import joblib

class ProphetForecaster:
    def __init__(self, game: str):
        self.game = game
        self.model = None
        
    def fit(self, draws_df: pd.DataFrame):
        df = draws_df[['draw_date', 'jackpot_amount']].copy()
        df.columns = ['ds', 'y']
        df = df.dropna()
        self.model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        self.model.fit(df)
        return self.model
    
    def forecast(self, periods: int = 10) -> pd.DataFrame:
        future = self.model.make_future_dataframe(periods=periods)
        return self.model.predict(future)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    def save(self, path):
        joblib.dump(self.model, path)
    
    def load(self, path):
        self.model = joblib.load(path)
