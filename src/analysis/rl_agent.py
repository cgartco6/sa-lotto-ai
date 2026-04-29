import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
from stable_baselines3 import PPO

class LotteryBettingEnv(Env):
    def __init__(self, game_params: dict, initial_bankroll: float = 10000):
        super().__init__()
        self.game_params = game_params
        self.initial_bankroll = initial_bankroll
        self.bankroll = initial_bankroll
        self.current_jackpot = 1000000
        self.draws_remaining = 52
        self.rollover_count = 0
        self.action_space = Discrete(4)
        self.observation_space = Box(low=0, high=1, shape=(4,), dtype=np.float32)
        
    def reset(self):
        self.bankroll = self.initial_bankroll
        self.current_jackpot = 1000000
        self.draws_remaining = 52
        self.rollover_count = 0
        return self._get_observation()
    
    def _get_observation(self):
        return np.array([
            self.bankroll / self.initial_bankroll,
            min(1.0, self.current_jackpot / 100000000),
            min(1.0, self.rollover_count / 20),
            self.draws_remaining / 52
        ], dtype=np.float32)
    
    def step(self, action):
        self.draws_remaining -= 1
        ticket_cost = 5
        tickets_bought = [0,1,5,10][action]
        cost = tickets_bought * ticket_cost
        if cost > self.bankroll:
            cost = self.bankroll
            tickets_bought = cost // ticket_cost
        self.bankroll -= cost
        winning_prob = min(0.01, 1/(self.game_params['main_max']**self.game_params['main_count']))
        reward = -cost
        if np.random.random() < winning_prob * tickets_bought:
            win_amount = self.current_jackpot / max(1, tickets_bought)
            self.bankroll += win_amount
            reward += win_amount
            self.rollover_count = 0
            self.current_jackpot = 1000000
        else:
            self.rollover_count += 1
            self.current_jackpot *= 1.2
        done = self.draws_remaining <= 0 or self.bankroll <= 0
        return self._get_observation(), reward, done, {}
    
    def render(self, mode='human'):
        pass

class RLBettingAgent:
    def __init__(self, game_params: dict):
        self.game_params = game_params
        self.env = LotteryBettingEnv(game_params)
        self.model = None
        
    def train(self, total_timesteps: int = 100000):
        self.model = PPO('MlpPolicy', self.env, verbose=1)
        self.model.learn(total_timesteps=total_timesteps)
        return self.model
    
    def get_bet_advice(self, bankroll: float, jackpot: float, rollovers: int) -> dict:
        if self.model is None:
            return {"advice": "Skip this draw", "action": 0, "tickets": 0}
        obs = np.array([
            bankroll / 10000,
            min(1.0, jackpot / 100000000),
            min(1.0, rollovers / 20),
            1.0
        ], dtype=np.float32)
        action, _ = self.model.predict(obs)
        tickets_map = {0:0, 1:1, 2:5, 3:10}
        return {
            "advice": ["Skip", "1 ticket", "5 tickets", "10 tickets"][action],
            "action": action,
            "tickets": tickets_map[action]
        }
