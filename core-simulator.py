
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
        """
        state array:
        - network found: 0 | 1
        - drone status: (0, operational), (1, DOS), (2, crashed), (3, controlled)
        - signal strength: -100 -> 0
        - crack progress: 0.0 -> 1.0 (0% to 100%)
        - time since success: 0.0 -> inf (time since a meaningful action was successful)
        """
                
        # observation space
        self.observation_space = Dict({
            "network_found" : Discrete(2), # network found, True 1, False 0
            "joined_network" : Discrete(2) # is the agent on the network?
            "drone_status" : Discrete(4), # 0: operational, 1: DOS, 2: crashed, 3: controlled
            "signal_strength_dbm" : Box(low=-100.0, high=0.0, shape=(), dtype=np.float32), # RSSI -100 => 0
            "cracking_progress" : Box(low=0.0, high=1.0, shape=(), dtype=np.float32), # 0.0 => 1.0
            "time_since_success" : Box(low=0.0, high=np.inf) # time since a meaningful action
        })

        # action space
        self.action_space = Dict({
            "search_networks" : search_networks,
            "join_network" : join_network,
            "capture_wpa_pskey" : capture_wpa_pskey,
            "crack_password" : crack_password,
            "flood_port" : flood_port,
            "wait" : wait,
            "change_network_password" : change_network_password,
            "land_drone" : land_drone,
            "crash_drone" : crash_drone,
            "jam_signals" : jam_signals
        })

        self.state = Dict({
            "has_password" : Discrete(2), # does the drone network have a password.
            "password_in_list" : Discrete(2), # is the drone password in the attacking dictionary list?
        }) # information about the drone env that is used to derive all observations about the env.


        self.current_obs = None
        self.current_step = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        """
        Reset the environment to initial states.
        """
        init_network_status = 0 # not found
        init_drone_status = 0 # operational
        init_rssi = self.np_random.uniform(low=-100.0, high=-85.0) # low signal strength. Drone is far away. 
        init_crack_progress = 0.0 # 0% progress.
        init_time_since_success = 0.0 # start of episode

        self.current_obs = np.array([
            init_network_status,
            init_drone_status,
            init_rssi,
            init_crack_progress,
            init_time_since_success
        ], dtype=np.float)

        self.current_step = 0
        info = {}
        return self.current_obs, info

    def step(self, action: str):
        """
        Takes an action from an agent and updates the environment.
        Give the agent new observations.
        """
        
        reward =0.05
        terminated = False
        truncated = False
        info = {}

        #unpack current observation
        net_found, drone_status, rssi, crack_progress, time_since_success = self.current_obs

        # maximum episode (truncation)
        if self.current_step >= 500:
            truncated = True

        # process the action
        action_function = self.action_space.get(action)
        if action_function:
            action_function(self)

        # get the observation
        observation = self._obs()

        return observation, reward, terminated, truncated, info

    def _obs(self):
        """
        Returns the observation of the environment. Uses self.state to determine the current observation.
        """
        pass

    def update_state(self):
        pass