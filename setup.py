import gymnasium as gym
from core_simulator import drone_env

gym.register(
    id='DroneHackingEnv-v0',
    entry_point='core_simulator:drone_env', 
    
)