import numpy as np
from tqdm import tqdm
from src.config import Config

class MonteCarloSimulator:
    def __init__(self, game: str):
        self.game = game
        self.main_max = Config.GAME_PARAMS[game]["main_max"]
        self.main_count = Config.GAME_PARAMS[game]["main_count"]
    
    def simulate_draw(self) -> set:
        return set(np.random.choice(range(1, self.main_max+1), self.main_count, replace=False))
    
    def hit_probability(self, wheel_tickets: list, n_simulations: int = Config.MC_SIMULATIONS) -> float:
        hits = 0
        for _ in tqdm(range(n_simulations), desc="Monte Carlo"):
            draw = self.simulate_draw()
            for ticket in wheel_tickets:
                if len(set(ticket) & draw) >= Config.WHEEL_GUARANTEE:
                    hits += 1
                    break
        return hits / n_simulations
