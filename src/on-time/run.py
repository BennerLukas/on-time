# install tensorflow beforehand manually
# install CUDA manually - for GPU support conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 (https://www.tensorflow.org/install/pip#windows_1)
import gym
import ray
from ray import tune
import os

# from base import Grid

# configuration and init
ray.init(ignore_reinit_error=True)
log_dir = "log_run"
log_path = os.path.join(os.getcwd(), log_dir)
# env = Grid()
env = gym.make('gym_example/gym_examples/GridWorld-v0')
seed = 123
max_iter = 100
# print(env.render())
##########################################################################################

# run without GPU
print("--Start RL--")
tune.run("DQN",
         config={
             "env": env,
             "num_gpus": 0,  # with gpu
             "seed": seed,
             # "evaluation_interval": 2,
             # "evaluation_duration": 10
         },
         local_dir=log_dir,
         name="with_GPU",
         verbose=3,
         stop=ray.tune.stopper.MaximumIterationStopper(max_iter)#,
         # time_budget_s=100
         )

pass
