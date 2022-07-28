# install tensorflow beforehand manually
# install CUDA manually - for GPU support conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 (https://www.tensorflow.org/install/pip#windows_1)
import gym
import ray
from ray import tune
import os


# import gridworld_mannheim_gym

# from base import Grid


def env_creator():
    from gridworld_gym.envs import GridWorldEnv as env
    return env


# configuration and init
log_dir = "src/on-time/log_run"
log_path = os.path.join(os.getcwd(), log_dir)
# env = Grid()
# env = gym.make('gridworld_gym:gridworld-v0')
ray.init(local_mode=True, ignore_reinit_error=True)
seed = 123
max_iter = 100
# print(env.render())
##########################################################################################

# run without GPU
print("--Start RL--")
tune.run("A3C",
         config={
             "env": env_creator(),
             "num_gpus": 0,  # with gpu
             "simple_optimizer":True
             # "seed": seed,
             # "evaluation_interval": 2,
             # "evaluation_duration": 10
         },
         local_dir=log_dir,
         name="with_GPU",
         verbose=3,

         stop=ray.tune.stopper.MaximumIterationStopper(max_iter)  # ,
         # time_budget_s=100
         )

pass
