# import ray
# from ray.rllib import agents
#
# ray.init()
# trainer = agents.a3c.A2CTrainer(env='CartPole-v0')
#
# trainer = agents.dqn.DQNTrainer(env='CartPole-v0') # Deep Q Network
#
# import ray
# from ray.rllib import agents
# ray.init() # Skip or set to ignore if already called
# config = {'gamma': 0.9,
#           'lr': 1e-2,
#           'num_workers': 4,
#           'train_batch_size': 1000,
#           'model': {
#               'fcnet_hiddens': [128, 128]
#           }}
# trainer = agents.ppo.PPOTrainer(env='CartPole-v0', config=config)
# results = trainer.train()


import ray
ray.init()

@ray.remote
def f(x):
    return x * x

futures = [f.remote(i) for i in range(4)]
print(ray.get(futures))