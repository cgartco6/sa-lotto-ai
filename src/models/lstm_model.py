import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class LottoLSTM:
    def __init__(self, sequence_length: int, n_features: int = 1):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = None
    
    def build_model(self):
        self.model = Sequential([
            LSTM(128, return_sequences=True, input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.2),
            LSTM(64, return_sequences=True),
            Dropout(0.2),
            LSTM(32),
            Dropout(0.2),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')
        return self.model
    
    def train(self, X, y, epochs=50, batch_size=32, validation_split=0.2):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=validation_split, verbose=1)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def save(self, path):
        self.model.save(path)
    
    def load(self, path):
        self.model = tf.keras.models.load_model(path)
