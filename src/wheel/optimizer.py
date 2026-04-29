class WheelOptimizer:
    @staticmethod
    def optimize_coverage(tickets: list, target_coverage: float = 0.95) -> list:
        unique = list(set(tickets))
        return unique[:int(len(unique)*0.7)]
