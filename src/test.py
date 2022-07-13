import ray
from ray.rllib import agents

ray.init()
trainer = agents.a3c.A2CTrainer(env='CartPole-v0')

trainer = agents.dqn.DQNTrainer(env='CartPole-v0') # Deep Q Network