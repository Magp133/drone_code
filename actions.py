"""
File containing the different actions that can be taken.
"""

import gymnasium as gym


def search_networks(env: gym.Env):
    """
    Given the information within the state of the environment,
    determine if a network is found and update the state.
    """


def capture_wpa_pskey(env: gym.Env):
    """
    Given the information within the state of the environment,
    determine if sending a deauthenticaiton packet to client on the
    found network successfully captures the wpa_pskey. 
    """

def crack_password(env: gym.Env):
    """
    Given the information within the state of the environment,
    start the process of cracking the password.
    """

def perform_dos(env: gym.Env):
    """
    Given the information within the state of the environment,
    start the process of a DOS on the drone. 
    """
