# install tensorflow beforehand manually
# install CUDA manually - for GPU support conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 (https://www.tensorflow.org/install/pip#windows_1)
import gym
import ray
from ray import tune
import os
import gridworld_gym
from gridworld_gym.envs import GridWorldEnv as env_creator

# configuration and init
log_dir = "logs/"
log_path = os.path.join(os.getcwd(), log_dir)
# env = gym.make("gridworld-v0")
RAY_IGNORE_UNHANDLED_ERRORS = 1
ray.init(local_mode=True, ignore_reinit_error=True)  # local_mode=True when no GPU is available
seed = 123
max_iter = 1000
# print(env.render(mode='human', close=False))
##########################################################################################

# run without GPU
print("--Start RL--")
tune.register_env("gridworld-v0", env_creator)

tune.run("PPO",
         config={
             "env": "gridworld-v0",
             "num_gpus": 0,  # 1 => with gpu
             "seed": seed,
             # "evaluation_interval": 2,
             # "evaluation_duration": 10,
             "horizon": 400,
             "soft_horizon": False,
             # "ignore_worker_failures": True,

         },
         local_dir=log_dir,
         # name="OnTime-RL",
         verbose=3,
         stop=ray.tune.stopper.MaximumIterationStopper(max_iter)  # ,
         # time_budget_s=100
        ,reuse_actors=True
         )

pass
