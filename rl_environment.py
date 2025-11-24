#!/usr/bin/env python3
"""
Reinforcement Learning environment for trading
"""

import gym
import numpy as np
from typing import Tuple

class TradingEnvironment(gym.Env):
    def __init__(self, api_connector):
        super(TradingEnvironment, self).__init__()
        self.api = api_connector
        self.symbol = "WINFUT"  # winFUT
        self.current_step = 0
        self.max_steps = 1000
        self.initial_balance = 10000
        self.balance = self.initial_balance
        self.position = 0  # 0: no position, 1: long, -1: short
        self.entry_price = 0

        # Action space: 0=hold, 1=buy, 2=sell
        self.action_space = gym.spaces.Discrete(3)

        # State space: [price, volume, balance, position]
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)

    def reset(self) -> np.ndarray:
        self.current_step = 0
        self.balance = self.initial_balance
        self.position = 0
        self.entry_price = 0
        return self._get_state()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, dict]:
        reward = 0
        done = False

        # Get current market data
        data = self.api.get_real_time_data(self.symbol)
        price = data.get("price", 100.0)

        # Execute action
        if action == 1:  # Buy
            if self.position == 0:
                self.position = 1
                self.entry_price = price
                reward = -1  # Small cost for transaction
        elif action == 2:  # Sell
            if self.position == 1:
                profit = price - self.entry_price
                self.balance += profit
                self.position = 0
                reward = profit  # Reward based on profit
            elif self.position == 0:
                self.position = -1
                self.entry_price = price
                reward = -1  # Transaction cost

        self.current_step += 1
        if self.current_step >= self.max_steps:
            done = True

        return self._get_state(), reward, done, {}

    def _get_state(self) -> np.ndarray:
        data = self.api.get_real_time_data(self.symbol)
        price = data.get("price", 100.0)
        volume = data.get("volume", 1000)
        return np.array([price, volume, self.balance, self.position], dtype=np.float32)