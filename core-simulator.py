
import gymnasium as gym
from gymnasium import spaces
import numpy as np



actions = {
    0 : "search", # search for networks
    1 : "start_injection", # start the injection chain
    2 : "start_dos", # start the dos chain
    3 : "capture_wpa_pskey", # attempt to capture the wpa network passkey
    4 : "retry_wpa_capture", # retry the attempt
    5 : "crack_password", # attempt to get the password through dict attack on the wpa passkey
    6 : "join_network", # attempt to join the drone network 
    7 : "change_network_password", # change the drone networks password
    8 : "flood_port", # flood the drones communication port
}

class drone_env(gym.Env):
    """
    Environment for interacting with a tello drone. 

    Designed to train policies for taking control of or DOS a drone. 
    Abstract functions are used for actions within the env. 
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
        # [network found (0/1), Drone status (0-3), RSSI/ signal strength (-100, 0), Crack progress (0.0-1.0), Time since success (0.0 - inf)]
        low = np.array([0, 0, -100, 0.0, 0.0])
        high = np.array([1, 3, 0, 1.0, np.inf])
        
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)


        self.current_obs = None
        self.current_step = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        """
        Reset the environment to initial states.
        """
        init_network_status = 0 # not found
        init_drone_status = 0 # operational
        init_rssi = np.random.randf(-100.0, -85) # low signal strength. Drone is far away. 
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

    def step(self, action):
        pass

    def _obs(self):
        pass
