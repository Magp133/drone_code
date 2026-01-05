import os
from ray.rllib.algorithms.ppo import PPO
from ray.tune.registry import register_env
from core_simulator import drone_env

from helper import *

def env_creator(env_config):
    return drone_env()
ENV_NAME = "DroneHackingEnv-v0"
register_env(ENV_NAME, env_creator)

env = drone_env()
obs, info = env.reset()


checkpoint_path = os.path.abspath("checkpoints")
algo = PPO.from_checkpoint(checkpoint_path)

print("--- Starting Inference Test ---")
print(f"Internal state: {env.state}")
done = False
total_reward = 0

while not done:
    # Tell the agent to pick the BEST action (explore=False)
    action = algo.compute_single_action(observation=obs, explore=False)
    
    # Run the action in the real simulator
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Print the specific action taken for debugging
    print(calculate_success_prob(env=env))
    print(f"Action: {action} | Reward: {reward} | Drone Status: {env.state['drone_status']}")
    
    total_reward += reward
    done = terminated or truncated

print(f"Test Finished. Total Reward: {total_reward}")
print(f"Internal state: {env.state}")