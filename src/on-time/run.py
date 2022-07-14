# install tensorflow beforehand manually
# install CUDA manually - for GPU support conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0 (https://www.tensorflow.org/install/pip#windows_1)
import ray
from ray import tune
import os

from base import Grid

# configuration and init
ray.init(ignore_reinit_error=True)
log_dir = "log_run"
log_path = os.path.join(os.getcwd(), log_dir)
env = Grid()
seed = 123
max_iter = 100
##########################################################################################

# run without GPU
print("--Start RL with GPU--")
tune.run("DQN",
         config={
             "env": env,
             "num_gpus": 1,  # with gpu
             "seed": seed,
             # "evaluation_interval": 2,
             # "evaluation_duration": 10
         },
         local_dir=log_dir,
         name="with_GPU",
         stop=ray.tune.stopper.MaximumIterationStopper(max_iter),
         # time_budget_s=100
         )

pass
