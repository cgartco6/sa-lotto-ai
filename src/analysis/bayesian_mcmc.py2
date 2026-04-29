import pymc as pm
import numpy as np
import pandas as pd
import arviz as az

class BayesianMCMC:
    def __init__(self, game: str, max_number: int):
        self.game = game
        self.max_number = max_number
        self.trace = None
        self.model = None
        
    def build_model(self, draws_df: pd.DataFrame):
        counts = np.zeros(self.max_number)
        for numbers in draws_df['numbers']:
            for num in numbers:
                counts[num-1] += 1
        with pm.Model() as model:
            alphas = pm.Gamma('alphas', alpha=2, beta=1, shape=self.max_number)
            betas = pm.Gamma('betas', alpha=2, beta=1, shape=self.max_number)
            probabilities = pm.Beta('probabilities', alpha=alphas, beta=betas, shape=self.max_number)
            obs = pm.Multinomial('obs', n=len(draws_df), p=probabilities, observed=counts)
        self.model = model
        return model
    
    def sample_posterior(self, draws: int = 2000, tune: int = 1000):
        with self.model:
            self.trace = pm.sample(draws=draws, tune=tune, return_inferencedata=True)
        return self.trace
    
    def get_probabilities(self) -> np.ndarray:
        if self.trace is None:
            raise ValueError("Run sample_posterior first")
        probs = self.trace.posterior['probabilities'].mean(dim=['chain', 'draw']).values
        return probs / probs.sum()
    
    def predict_top_n(self, n: int = 13) -> list:
        probs = self.get_probabilities()
        top_indices = np.argsort(probs)[::-1][:n]
        return [idx+1 for idx in top_indices]
