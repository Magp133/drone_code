import os
import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

# Import your environment class
from core_simulator import drone_env 

def env_creator(env_config):
    return drone_env()

# 1. Register the environment with a unique name
ENV_NAME = "DroneHackingEnv-v0"
register_env(ENV_NAME, env_creator)

def train():
    # remove old workers maybe?
    ray.shutdown()
    ray.init(ignore_reinit_error=True)

    config = PPOConfig()
    config = config.environment(env=ENV_NAME)
    config = config.framework("torch") 
    config = config.resources(num_gpus=0)
    config = config.env_runners(num_env_runners=1) 
    config = config.api_stack(enable_env_runner_and_connector_v2=False, enable_rl_module_and_learner=False)

    # UPDATED TRAINING BLOCK
    config = config.training(
        lr=5e-5,
        gamma=0.99,
        lambda_=0.95,
        clip_param=0.2,
        # Fix: 'sgd_minibatch_size' is now 'minibatch_size'
        minibatch_size=64, 
        train_batch_size=4000,
    )

    config = config.evaluation(
        evaluation_interval=5,
        evaluation_duration=10,
        
        evaluation_config={"explore": False},
    )

    algo = config.build()
    # 5. Training Loop
    print(f"--- Starting Training on {ENV_NAME} ---")
    checkpoint_dir = "checkpoints"
    
    for i in range(50):  # Total training iterations
        result = algo.train()
        
        # Print key metrics
        print(f"Iteration: {i}")
        print(f"  -- Mean Reward: {result['env_runners']['episode_reward_mean']:.2f}")
        print(f"  -- Entropy:  {result['info']['learner']['default_policy']['learner_stats']['entropy']:.2f}")
        print(f"  -- Policy Loss: {result['info']['learner']['default_policy']['learner_stats']['policy_loss']}")
        print(f"  -- Value Loss: {result['info']['learner']['default_policy']['learner_stats']['vf_loss']}")
        print(f"  -- Episode Length Mean: {result['env_runners']['episode_len_mean']}")
        # print(result)

        # Save checkpoint every 10 iterations
        if i % 10 == 0:
            checkpoint_path = algo.save(checkpoint_dir)
            print(f"      Checkpoint saved at: {checkpoint_path}")

    print("Training complete.")
    ray.shutdown()

if __name__ == "__main__":
    train()