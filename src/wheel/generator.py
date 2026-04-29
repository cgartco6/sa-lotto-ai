from itertools import combinations
from typing import List, Tuple

class WheelGenerator:
    def __init__(self, numbers: List[int], line_length: int = 6):
        self.numbers = sorted(numbers)
        self.line_length = line_length
    
    def generate_full_wheel(self) -> List[Tuple]:
        return list(combinations(self.numbers, self.line_length))
    
    def generate_abbreviated_wheel(self, picked: int = 6, guarantee: int = 4) -> List[Tuple]:
        all_combs = list(combinations(self.numbers, self.line_length))
        return all_combs[:50]  # simplified
