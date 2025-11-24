#!/usr/bin/env python3
"""
RL Agent using DQN for trading decisions
"""

import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

class RLAgent:
    def __init__(self, env):
        self.env = DummyVecEnv([lambda: env])
        self.model = DQN("MlpPolicy", self.env, verbose=1, learning_rate=0.001)

    def train(self, episodes: int = 1000):
        """Train the RL model"""
        self.model.learn(total_timesteps=episodes)

    def predict(self, state: np.ndarray) -> int:
        """Make a prediction based on current state"""
        action, _ = self.model.predict(state)
        return action

    def save_model(self, path: str):
        """Save the trained model"""
        self.model.save(path)

    def load_model(self, path: str):
        """Load a trained model"""
        self.model = DQN.load(path, env=self.env)