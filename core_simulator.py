
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from gymnasium.spaces import Box, Dict, Tuple, Discrete, MultiBinary, utils
from actions import *

import ray


class drone_env(gym.Env):
    """
    Environment for interacting with a tello drone. 

    Designed to train policies for taking control of or DOS a drone. 
    Abstract functions are used for actions within the env. 

    Check cyborg default wrapper. 
    """
    def __init__(self):    
        # observation space
        self.observation_space = Dict({
            "network_found" : Discrete(2), # network found, True 1, False 0
            "joined_network" : Discrete(2), # is the agent on the network?
            "drone_status" : Discrete(4), # 0: operational, 1: DOS, 2: crashed, 3: controlled
            "signal_strength_dbm" : Box(low=-100.0, high=0.0, shape=(), dtype=np.float32), # RSSI -100 => 0
            "cracking_progress" : Box(low=0.0, high=1.0, shape=(), dtype=np.float32) # 0.0 => 1.0
            })

        # action space
        self.action_space = Dict(spaces={
            "search_networks" : Discrete(2),
            "join_network" : Discrete(2),
            "capture_wpa_pskey" : Discrete(2),
            "crack_password" : Discrete(2),
            "flood_port" : Discrete(2),
            "change_network_password" : Discrete(2),
            "land_drone" : Discrete(2),
            "crash_drone" : Discrete(2),
            "jam_signals" : Discrete(2)
        })

        self.state = {
            "drone_status" : 0, # 0, operational, 1 controlled, 2 crashed, 3 landed
            "found_network" : False, # has the agent identified a drone network. 
            "on_drone_network" : False, # is the agent connected to the drone's network.
            "network_has_password" : self.np_random.choice([True, False]), # determine if the drone network is password protected. 
            "password_list_has_password" : self.np_random.choice([True, False]), # determine if the drone's network password is contained by the password list.
            "signal_strength" : -100, # signal strength of the drone. Starts far away. 
            "password_cracking_started" : False, # has the password cracking began
            "password_cracking_progress" : 0.0, # cracking progress of the password
            "has_wpa_pskey" : False, # has the agent found the wpa pskey.
            "last_action" : None, # stores the last action
            "action_success" : False, # did the last action succeed. 
            "target_port_vulnerable" : self.np_random.choice([True, False]), # is the target port vulnerable to dos flooding attack. 

        }

        self.current_obs = None
        self.current_step = 0

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        """
        Reset the environment to initial states.
        """
        self.state["drone_status"] = "operational"
        self.state["found_network"] = False
        self.state["on_drone_network"] = False
        
        self.state["network_has_password"] = self.np_random.choice([True, False]) 
        self.state["password_list_has_password"] = self.np_random.choice([True, False]) 
        self.state["signal_strength"] = self.np_random.uniform(low= -100.0, high= -85.0) 
        
        self.state["password_cracking_progress"] = 0.0
        self.state["has_wpa_pskey"] = False
        self.state["password_cracking_started"] = False
        self.state["target_port_vulnerable"] = self.np_random.choice([True, False])
        


        self.current_step = 0
        info = {}
        observation = self._obs()

        return observation, info

    def step(self, action: dict):
        """
        Takes an action from an agent and updates the environment.
        Give the agent new observations.

        Need to change to disallow multiple actions taken during a single step. 
        """
        

        reward =0.05
        terminated = False
        truncated = False
        info = {}

        # get the action space
        search_networks = action["search_networks"]
        join_network = action["join_network"]
        capture_wpa_pskey = action["capture_wpa_pskey"]
        crack_password = action["crack_password"]
        flood_port = action["flood_port"]
        change_network_password = action["change_network_passwordd"]
        land_drone = action["land_drone"]
        crash_drone = action["crash_drone"]
        jam_signals = action["jam_signals"]

        # ensure that there is only 1 action that can be taken.

        active_actions = sum(action.values())

        if active_actions > 1:
            reward = -10
            truncated = True
            info["error"] = "Tried doing multiple actions at the same time."

        elif search_networks == 1:
            func_reward = search_for_drone_network(self)
            reward += func_reward

        elif join_network == 1:
            func_reward = join_drone_network(self)
            reward += func_reward

        elif capture_wpa_pskey == 1:
            func_reward = capture_drone_wpa_pskey(self)
            reward += func_reward
        
        elif crack_password == 1:
            func_reward = crack_drone_password(self)
            reward += func_reward
        
        elif flood_port == 1:
            func_reward = flood_drone_port(self)
            reward += func_reward

        elif change_network_password == 1:
            func_reward = change_drone_network_password(self)
            reward += func_reward

        elif land_drone == 1:
            func_reward = land_drone_func(self)
            reward += func_reward

        elif crash_drone == 1:
            func_reward = crash_drone_func(self)
            reward += func_reward
        
        elif jam_signals == 1:
            func_reward = jam_drone_signals(self)
            reward += func_reward
        

        # get the observation and update the overall internal state. 
        observation = self._obs()
        self.update_state()

        self.current_step += 1

        if self.current_step >= 500:
            truncated = True

        if self.state["drone_status"] == 2 or self.state["drone_status"] == 3: # drone has crashed or landed
            terminated = True

        return observation, reward, terminated, truncated, info

    def _obs(self):
        """
        Returns the observation of the environment. Uses self.state to determine the current observation.
        """

        self.current_obs = np.array([
            self.state["found_network"],
            self.state["on_drone_network"],
            self.state["drone_status"],
            self.state["signal_strength"],
            self.state["password_cracking_progress"],
        ], dtype=np.float32)
        
        return self.current_obs

    def update_state(self):
        pass