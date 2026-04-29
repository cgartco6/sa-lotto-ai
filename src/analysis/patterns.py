import pandas as pd
import numpy as np

class PatternAnalyzer:
    @staticmethod
    def detect_sequences(draws_df: pd.DataFrame, seq_len: int = 3) -> list:
        sequences = []
        for numbers in draws_df['numbers']:
            sorted_nums = sorted(numbers)
            for i in range(len(sorted_nums) - seq_len + 1):
                if sorted_nums[i+seq_len-1] - sorted_nums[i] == seq_len - 1:
                    sequences.append(tuple(sorted_nums[i:i+seq_len]))
        return sequences
    
    @staticmethod
    def hot_cold_zones(freq_dict: dict, threshold_percentile: int = 80) -> tuple:
        freqs = list(freq_dict.values())
        hot_threshold = np.percentile(freqs, threshold_percentile)
        cold_threshold = np.percentile(freqs, 20)
        hot = [num for num, f in freq_dict.items() if f >= hot_threshold]
        cold = [num for num, f in freq_dict.items() if f <= cold_threshold]
        return hot, cold
