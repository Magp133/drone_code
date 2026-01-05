"""
File containing the different actions that can be taken.
"""
import numpy as np
from helper import *


def search_for_drone_network(env) -> float:
    """
    Given the information within the state of the environment,
    determine if a network is found and update the state.

    action 0
    """
    # if the network has already been found then return small penalty.
    if env.state["found_network"]:
        return -0.5


    if np.random.random() < calculate_success_prob(env=env):
        env.state["found_network"] = True
        return 1.0
    else:
        return -0.1

def join_drone_network(env) -> float:
    """
    Given information within the state of the environment,
    attempt to join the drone network.

    action 1
    """
    
    if not env.state["found_network"]:
        return -1.0

    if env.state["on_drone_network"]:
        return -1.0
    
    
    # check if the network has a password.
    # if so then does the agent also have the password to get on the network?
    if env.state["network_has_password"]:
        if env.state["password_cracking_progress"] == 1.0:
            if np.random.random() < calculate_success_prob(env=env):
                env.state["on_drone_network"] = True
                return 1.0
            else:
                return -0.1
        else:
            return -1.0
    else:
        if np.random.random() < calculate_success_prob(env=env):
            env.state["on_drone_network"] = True
            return 1.0
        else:
            return -0.1

        

def capture_drone_wpa_pskey(env) -> float:
    """
    Given the information within the state of the environment,
    determine if sending a deauthenticaiton packet to client on the
    found network successfully captures the wpa_pskey. 

    action 2
    """

    if env.state["has_wpa_pskey"]:
        return -0.5

    # does the drone network have a password?
    # if not then penalise
    if not env.state["network_has_password"]:
        return -0.1
    
    if env.state["found_network"]:
        if np.random.random() < calculate_success_prob(env=env):
            env.state["has_wpa_pskey"] = True
            return 1.0
        
    return -0.5

def crack_drone_password(env) -> float:
    """
    Given the information within the state of the environment,
    start the process of cracking the password.

    action 3
    """

    if env.state["has_wpa_pskey"]:
        if env.state["password_cracking_started"]:
            return -0.1
        else:
            env.state["password_cracking_started"] = True
            return 1.0
    else:
        return -0.1


def flood_drone_port(env) -> float:
    """
    Given the information within the state of the environment,
    flood the communication port of the drone.
    Must be on the network.

    action 4
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

    action 5
    """

    if env.state["on_drone_network"]:
        if env.state["drone_status"] == 1:
            return -0.5
        if np.random.random() < 0.5:
            env.state["drone_status"] = 1 # drone is now controlled
            return 5.0

    return -0.1

def land_drone_func(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to land the drone through injection.
    (simulated)

    action 6
    """

    if env.state["on_drone_network"] and env.state["drone_status"] == 1: # agent is on drone network and drone is controlled.
        # trying to land doesnt always work.
        if np.random.random() < 0.5:
            env.state["drone_status"] = 3 # drone is landed.
            return 20.0
        else:
            return 0.1
    else:
        return -0.1

def crash_drone_func(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to crash the drone through injection.

    action 7
    """
    if env.state["on_drone_network"] and env.state["drone_status"] == 1:
        env.state["drone_status"] = 2 # drone is crashed.
        return 5.0
    return -0.1

def jam_drone_signals(env) -> float:
    """
    Given the information within the state of the environment,
    simulate jamming all signals in the area. 
    does not require being on the network. 

    action 8
    """
    env.state["drone_status"] = 2 # drone has crashed. 

    return 1.0

def wait(env) -> float:
    """
    wait one step.

    action 9
    """
    return -0.1