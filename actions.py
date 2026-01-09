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
    if env.state["found_network"]:
        return -2.0 # wasted move


    if np.random.random() < calculate_success_prob(env=env):
        env.state["found_network"] = True
        return 5.0 # success
    else:
        return -0.1

def join_drone_network(env) -> float:
    """
    Given information within the state of the environment,
    attempt to join the drone network.

    action 1
    """
    if not env.state["found_network"]:
        return -10.0 # really bad move
    
    if env.state["network_has_password"] and env.state["password_cracking_progress"] < 1.0:
        return -10.0 # Heavy penalty: Can't join without cracking

    if env.state["on_drone_network"]:
        return -2.0
    
    # the password list does not contain the password.
    # agent cannot join the network at all. 
    if not env.state["password_list_has_password"] and env.state["network_has_password"]:
        return -1.0
    
    # check if the network has a password.
    # if so then does the agent also have the password to get on the network?
    if np.random.random() < calculate_success_prob(env=env):
            env.state["on_drone_network"] = True
            return 10.0 # Reward for getting onto the network
    return -0.1

        

def capture_drone_wpa_pskey(env) -> float:
    """
    Given the information within the state of the environment,
    determine if sending a deauthenticaiton packet to client on the
    found network successfully captures the wpa_pskey. 

    action 2
    """
    if not env.state["found_network"]:
            return -10.0 # Heavy penalty: Prerequisite not met

    if env.state["has_wpa_pskey"]:
        return -2.0 # Wasted move

    if not env.state["network_has_password"]:
        return -5.0 # Error: Trying to steal a key that doesn't exist
    
    if np.random.random() < calculate_success_prob(env=env):
        env.state["has_wpa_pskey"] = True
        return 5.0 # Reward for capturing key
    return -0.5

def crack_drone_password(env) -> float:
    """
    Given the information within the state of the environment,
    start the process of cracking the password.

    action 3
    """
    if not env.state["has_wpa_pskey"]:
            return -10.0

    if env.state["password_cracking_started"]:
        return -2.0 # Wasted move if already running

    env.state["password_cracking_started"] = True
    return 5.0 # Reward for starting the cracking process


def flood_drone_port(env) -> float:
    """
    Given the information within the state of the environment,
    flood the communication port of the drone.
    Must be on the network.

    action 4
    """

    if not env.state["on_drone_network"]:
        return -10.0

    # Check if already neutralized
    if env.state["drone_status"] != 0: 
        return -2.0
    
    if env.state["target_port_vulnerable"]:
        env.state["drone_status"] = 2 # crashed
        return 10.0 # Significant reward for achieving a DoS
    else:
        return -2.0 # Penalty for attacking a non-vulnerable port

def change_drone_network_password(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to change the network password.

    action 5
    """
    if not env.state["on_drone_network"]:
        return -10. # bad move

    if env.state["drone_status"] == 1:
        return -2.0 # Already controlled

    # Attempt control
    if np.random.random() < 0.5:
        env.state["drone_status"] = 1 # controlled
        return 15.0 # High reward for gaining control

    return -0.5

def land_drone_func(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to land the drone through injection.
    (simulated)

    action 6
    """
    if env.state["drone_status"] != 1:
        return -10.0

    if np.random.random() < 0.5:
        env.state["drone_status"] = 3 # landed
        return 20.0 # Maximum reward for safest success
    else:
        return 0.1 # Small positive reinforcement for trying the right final step

def crash_drone_func(env) -> float:
    """
    Given the information within the state of the environment,
    attempt to crash the drone through injection.

    action 7
    """
    # Logical Prerequisite: Must have control (Action 5) first
    if env.state["drone_status"] != 1:
        return -10.0

    env.state["drone_status"] = 2 # crashed
    return 10.0 # Reward for mission completion via crash

def jam_drone_signals(env) -> float:
    """
    Given the information within the state of the environment,
    simulate jamming all signals in the area. 
    does not require being on the network. 

    action 8
    """
    env.state["drone_status"] = 2 
    return 2.0

def wait(env) -> float:
    """
    wait one step.

    action 9
    """
    if env.state["password_cracking_started"] and env.state["password_cracking_progress"] < 1.0:
        return 0.5 # acceptable action
    
    return -0.1 # General penalty for idling without a reason