
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from gymnasium.spaces import Box, Dict, Tuple, Discrete, MultiBinary, utils


from actions import *
from helper import *


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
        self.action_space = Discrete(10)
        
        # Define the mapping from index to function for the step method
        self.action_map = {
            0: search_for_drone_network,
            1: join_drone_network,
            2: capture_drone_wpa_pskey,
            3: crack_drone_password,
            4: flood_drone_port,
            5: change_drone_network_password,
            6: land_drone_func,
            7: crash_drone_func,
            8: jam_drone_signals,
            9: wait,
        }

        self.state = {
            "drone_status" : 0, # 0 operational, 1 controlled, 2 crashed, 3 landed
            "found_network" : False, # has the agent identified a drone network. 
            "on_drone_network" : False, # is the agent connected to the drone's network.
            "network_has_password" : self.np_random.choice([True, False]), # determine if the drone network is password protected. 
            "password_list_has_password" : self.np_random.choice([True, False]), # determine if the drone's network password is contained by the password list.
            "signal_strength" : -100, # signal strength of the drone. Starts far away. 
            "password_cracking_started" : False, # has the password cracking began
            "password_cracking_progress" : 0.0, # cracking progress of the password
            "has_wpa_pskey" : False, # has the agent found the wpa pskey.
            "target_port_vulnerable" : self.np_random.choice([True, False]), # is the target port vulnerable to dos flooding attack. 

        }

        self.current_obs = None
        self.current_step = 0

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        """
        Reset the environment to initial states.
        """
        self.state["drone_status"] = 0 # operational
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

        # confirm the action index is within the action map
        if action in self.action_map:
            action_func = self.action_map[action]

            reward += action_func(self)
        else:
            reward -= 10.0
            info["error"] = "Invalid action index"


        

        # get the observation and update the overall internal state. 
        observation = self._obs()
        self.update_state()

        self.current_step += 1

        if self.current_step >= 500:
            truncated = True

        if self.state["drone_status"] == 2 or self.state["drone_status"] == 3: # drone has crashed or landed
            terminated = True

        if self.state["signal_strength"] >= -5:
            # Drone has gotten too close to the defended target. 
            terminated = True

        return observation, reward, terminated, truncated, info

    def _obs(self):
        """
        Returns the observation of the environment. Uses self.state to determine the current observation.
        """

        self.current_obs = {
                "network_found" : int(self.state["found_network"]),
                "joined_network" : int(self.state["on_drone_network"]),
                "drone_status" : self.state["drone_status"], # Assuming status is an integer (0-3)
                "signal_strength_dbm": np.array(self.state["signal_strength"], dtype=np.float32),
                "cracking_progress": np.array(self.state["password_cracking_progress"], dtype=np.float32),
            }
        
        return self.current_obs

    def update_state(self):
        """
        Updates the internal states.
        Progresses certain actions/ changes states given newly made changes. 
        """
        increment_cracking(self)
        update_wpa_pskey(self)
        move_drone(self)