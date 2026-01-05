"""
Functions to help the rl agent or environment.
"""

import gymnasium as gym
import numpy as np
import math

def increment_cracking(env) -> None:
    """
    increments the cracking progress of the password cracking.
    """

    if env.state["password_cracking_started"] == True and env.state["password_cracking_progress"] < 1.0:
        env.state["password_cracking_progress"] += np.random.uniform(low=0.1, high=0.25)
    
    if env.state["password_cracking_progress"] > 1.0:
        env.state["password_cracking_progress"] = 1.0

def move_drone(env) -> None:
    """
    change the signal strength to represent the drone moving.
    """
    signal_change = np.random.uniform(low=-5.0, high=10.0)
    env.state["signal_strength"] += signal_change

    env.state["signal_strength"] = np.clip(env.state["signal_strength"], -100.0, 0.0)


def calculate_success_prob(env) -> float:
    """
    given an environments signal strength, calculate the chance of success.
    formula used is: $$P(s) = \frac{1}{1 + e^{-k(s - s_0)}}$$
    s: current signal strength,
    s_0: midpoint,
    k: steepness of the curve.
    """

    midpoint = -85 # -85db
    steepness = 0.3 # arbitrarily chosen

    signal_strength = env.state["signal_strength"] 

    # logistic equation
    prob = 1 / (1 + np.exp(-steepness * (signal_strength - midpoint)))

    return prob