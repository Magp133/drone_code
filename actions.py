"""
File containing the different actions that can be taken.
"""
import numpy as np


def search_for_drone_network(env) -> float:
    """
    Given the information within the state of the environment,
    determine if a network is found and update the state.
    """
    # if the network has already been found then return small penalty.
    if env.state["found_network"]:
        return -0.1
    
    signal_strength = env.state["signal_strength"]

    probability_of_success = (signal_strength + 100.0) / 100.0

    if np.random.random() < probability_of_success:
        env.state["found_network"] = True
        return 1.0
    else:
        return -0.1

def join_drone_network(env) -> float:
    """
    Given information within the state of the environment,
    attempt to join the drone network.
    """

    if env.state["on_drone_network"]:
        return -0.1
    
    signal_strength = env.state["signal_strength"]

    probability_of_success = (signal_strength + 100.0) / 100.0

    if np.random.random() < probability_of_success:
        env.state["on_drone_network"] = True
        return 1.0
    else:
        return -0.1

def capture_drone_wpa_pskey(env) -> float:
    """
    Given the information within the state of the environment,
    determine if sending a deauthenticaiton packet to client on the
    found network successfully captures the wpa_pskey. 
    """

    # check the prerequesites are met.
    if not env.state["found_network"] and not env.state["has_wpa_pskey"]:
        return -0.5

    # does the drone network have a password?
    if not env.state["network_has_password"]:
        return -0.1
    
    if np.random.random() < 0.5:
        env.state["has_wpa_pskey"] = True
        return 1.0
    else:
        return -0.1

def crack_drone_password(env) -> float:
    """
    Given the information within the state of the environment,
    start the process of cracking the password.
    """

    if not env.state["has_wpa_pskey"]:
        return -0.5
    else:
        env.state["password_cracking_started"] = True
        return 1.0


def flood_drone_port(env) -> float:
    """
    Given the information within the state of the environment,
    flood the communication port of the drone.
    Must be on the network.
    """
    if env.state["drone_status"] != 0 and env.state["on_drone_network"]: # drone is controlled, crashed or already dos
        return -0.1
    
    if env.state["target_port_vulnerable"]:
        env.state["drone_status"] = 2 # the drone has been crashed.
        return 1.0
    else:
        return -0.1

def change_drone_network_password(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to change the network password.
    """

    if env.state["on_drone_network"]:
        if np.random.random() < 0.5:
            env.state["drone_status"] = 1 # drone is now controlled
            return 5.0

    return -0.1

def land_drone_func(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to land the drone through injection.
    (simulated)
    """

    if env.state["on_drone_network"] and env.state["drone_status"] == 1: # agent is on drone network and drone is controlled.
        # trying to land doesnt always work.
        if np.random.random() < 0.5:
            env.state["drone_status"] = 3 # drone is landed.
            return 10.0
        else:
            return 0.1
    else:
        return -0.1

def crash_drone_func(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to crash the drone through injection.
    """
    if env.state["on_drone_network"] and env.state["drone_status"] == 1:
        env.state["drone_status"] = 2 # drone is crashed.
        return 5.0
    return -0.1

def jam_drone_signals(env) -> float:
    """
    Given the information within the state of the environment,
    simulate jamming all signals in the area. 
    massive penalty. does not require being on the network. 
    """
    env.state["drone_status"] = 2

    return -10.0

def wait(env) -> float:
    """
    wait one step.
    """
    return 0.0