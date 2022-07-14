import ray  # install tensorflow beforehand manually
# install CUDA manually - for GPU support

from ray import tune
import os

ray.init(ignore_reinit_error=True)
log_dir = "log_run"
log_path = os.path.join(os.getcwd(), log_dir)


# run without GPU
print("Start RL with GPU ")
tune.run("DQN",
         config={
             "env": "CartPole-v1",
             "num_gpus": 1,  # with gpu
             "seed": 123,
             # "evaluation_interval": 2,
             # "evaluation_duration": 10
         },
         local_dir=log_dir,
         name="with_GPU",
         stop=ray.tune.stopper.MaximumIterationStopper(10),
         # time_budget_s=100
         )

pass
