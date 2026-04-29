from collections import Counter
from itertools import combinations

class PairAnalyzer:
    @staticmethod
    def get_frequent_pairs(draws_df: pd.DataFrame, top_k: int = 20) -> list:
        pair_counter = Counter()
        for numbers in draws_df['numbers']:
            for pair in combinations(sorted(numbers), 2):
                pair_counter[pair] += 1
        return pair_counter.most_common(top_k)
