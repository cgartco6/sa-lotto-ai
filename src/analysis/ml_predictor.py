import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
from src.models.lstm_model import LottoLSTM
from src.analysis.frequency import FrequencyAnalyzer
from src.config import Config

class LotteryPredictor:
    def __init__(self, game: str):
        self.game = game
        self.model = None
        self.scaler = MinMaxScaler()
        self.sequence_length = Config.SEQUENCE_LENGTH
        
    def prepare_lstm_data(self, draws_df: pd.DataFrame):
        all_nums = []
        for nums in draws_df['numbers']:
            all_nums.extend(nums)
        all_nums = np.array(all_nums).reshape(-1, 1)
        scaled = self.scaler.fit_transform(all_nums)
        X, y = [], []
        for i in range(self.sequence_length, len(scaled)-1):
            X.append(scaled[i-self.sequence_length:i, 0])
            y.append(scaled[i, 0])
        return np.array(X), np.array(y)
    
    def train(self, draws_df: pd.DataFrame, epochs: int = Config.LSTM_EPOCHS):
        X, y = self.prepare_lstm_data(draws_df)
        if len(X) == 0:
            raise ValueError("Not enough data")
        X = X.reshape((X.shape[0], X.shape[1], 1))
        self.model = LottoLSTM(sequence_length=self.sequence_length, n_features=1)
        self.model.build_model()
        self.model.train(X, y, epochs=epochs, batch_size=Config.LSTM_BATCH_SIZE)
        joblib.dump(self.scaler, f"models/{self.game}_lstm_scaler.pkl")
        return self.model
    
    def predict_next_numbers(self, draws_df: pd.DataFrame, top_k: int = 13) -> list:
        """
        Real prediction using frequency analysis as fallback.
        (LSTM full prediction would require more complex sequence generation)
        """
        freq = FrequencyAnalyzer.get_number_frequencies(draws_df, 
                   max_num=Config.GAME_PARAMS[self.game]["main_max"])
        top_numbers = FrequencyAnalyzer.get_top_n(freq, top_k)
        return top_numbers
