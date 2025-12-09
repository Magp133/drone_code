"""
File containing the different actions that can be taken.
"""

import gymnasium as gym


def search_networks(env: gym.Env):
    """
    Given the information within the state of the environment,
    determine if a network is found and update the state.
    """

def join_network(env: gym.Env):
    """
    Given information within the state of the environment,
    attempt to join the drone network.
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

def flood_port(env: gym.Env):
    """
    Given the information within the state of the environment,
    flood the communication port of the drone.
    Must be on the network.
    """


def wait(env: gym.Env):
    """
    Given the information within the state of the environment,
    wait for processes to finish.
    """

def change_network_password(env: gym.Env):
    """
    Given the information within the state of the environment,
    attempt to change the network password.
    """

def land_drone(env: gym.Env):
    """
    Given the information within the state of the environment,
    attempt to land the drone through injection.
    (simulated)
    """

def crash_drone(env: gym.Env):
    """
    Given the information within the state of the environment,
    attempt to crash the drone through injection.
    """

def jam_signals(env: gym.Env):
    """
    Given the information within the state of the environment,
    simulate jamming all signals in the area. 
    massive penalty. does not require being on the network. 
    """