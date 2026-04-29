import pandas as pd
from collections import Counter

class FrequencyAnalyzer:
    @staticmethod
    def get_number_frequencies(draws_df: pd.DataFrame, max_num: int = 58) -> dict:
        all_numbers = []
        for numbers in draws_df['numbers']:
            all_numbers.extend(numbers)
        freq = Counter(all_numbers)
        return {num: freq.get(num, 0) for num in range(1, max_num+1)}
    
    @staticmethod
    def get_top_n(freq_dict: dict, n: int = 13) -> list:
        sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in sorted_items[:n]]
