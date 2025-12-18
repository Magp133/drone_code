"""
Functions to help the rl agent or environment.
"""

import gymnasium as gym
import numpy as np

def increment_cracking(env) -> None:
    """
    increments the cracking progress of the password cracking.
    """

    if env.state["password_cracking_started"] == True and env.state["password_cracking_progress"] < 1.0:
        env.state["password_cracking_progress"] += np.random.uniform(low=0.1, high=0.25)
    
    if env.state["password_cracking_progress"] > 1.0:
        env.state["password_cracking_progress"] = 1.

def update_wpa_pskey(env) -> None:
    """
    updates the internal state of the wpa_pskey for the agent.
    """
    if env.state["password_cracking_progress"] >= 1.0:
        if env.state["password_list_has_password"]:
            env.state["has_wpa_pskey"] = True

def move_drone(env) -> None:
    """
    change the signal strength to represent the drone moving.
    """
    signal_change = np.random.uniform(low=-5.0, high=10.0)
    env.state["signal_strength"] += signal_change