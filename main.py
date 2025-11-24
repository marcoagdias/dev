#!/usr/bin/env python3
"""
Main application for RL-based trading predictions
"""

import logging
from api_connector import APIConnector
from rl_environment import TradingEnvironment
from rl_agent import RLAgent
from prediction_system import PredictionSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize components
    api = APIConnector()
    env = TradingEnvironment(api)
    agent = RLAgent(env)
    predictor = PredictionSystem(agent, api)

    # Train on historical data
    logger.info("Starting training on historical data...")
    agent.train(episodes=1000)

    # Start real-time predictions
    logger.info("Starting real-time predictions...")
    predictor.run()

if __name__ == "__main__":
    main()