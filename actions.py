"""
File containing the different actions that can be taken.
"""

import gymnasium as gym


def search_for_drone_network(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    determine if a network is found and update the state.
    """

    return 0.0

def join_drone_network(env: gym.Env) -> float:
    """
    Given information within the state of the environment,
    attempt to join the drone network.
    """

    return 0.0

def capture_drone_wpa_pskey(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    determine if sending a deauthenticaiton packet to client on the
    found network successfully captures the wpa_pskey. 
    """

    return 0.0

def crack_drone_password(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    start the process of cracking the password.
    """

    return 0.0

def flood_drone_port(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    flood the communication port of the drone.
    Must be on the network.
    """

    return 0.0

def change_drone_network_password(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    attempt to change the network password.
    """

    return 0.0

def land_drone_func(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    attempt to land the drone through injection.
    (simulated)
    """

    return 0.0

def crash_drone_func(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    attempt to crash the drone through injection.
    """

    return 0.0

def jam_drone_signals(env: gym.Env) -> float:
    """
    Given the information within the state of the environment,
    simulate jamming all signals in the area. 
    massive penalty. does not require being on the network. 
    """

    return 0.0