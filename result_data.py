import os
from ray.rllib.algorithms.ppo import PPO
from ray.tune.registry import register_env
from core_simulator import drone_env
import pandas as pd

from pprint import pprint

from helper import *

def env_creator(env_config):
    return drone_env()
ENV_NAME = "DroneHackingEnv-v0"
register_env(ENV_NAME, env_creator)



env = drone_env()
checkpoint_path = os.path.abspath("checkpoints")
algo = PPO.from_checkpoint(checkpoint_path)

data_out = []

for i in range(100):
    obs, info = env.reset()
    done = False
    total_reward = 0
    step_count = 0

    while not done:
        # Tell the agent to pick the BEST action (explore=False)
        action = algo.compute_single_action(observation=obs, explore=False)
        
        # Run the action in the real simulator
        obs, reward, terminated, truncated, info = env.step(action)
        
        data_out.append({
                    "episode": i,
                    "step": step_count,
                    "action": action,
                    "reward": reward,
                    "drone_status": env.state['drone_status'],
                    "terminated": terminated,
                    "network_has_password" : env.state["network_has_password"],
                    "password_list_has_password" : env.state["password_list_has_password"],
                    "target_port_vulnerable" : env.state["password_list_has_password"]
                })

        total_reward += reward
        step_count += 1
        done = terminated or truncated

df = pd.DataFrame(data_out)
# print(df.head())

df.to_csv("results/output.csv")