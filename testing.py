from core_simulator import *
from setup import *

from gymnasium.utils.env_checker import check_env

gym.register(
    id='DroneHackingEnv-v0',
    entry_point='core_simulator:drone_env', 
    
)

env = gym.make('DroneHackingEnv-v0')
check_env(env)