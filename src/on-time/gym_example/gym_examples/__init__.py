from gym.envs.registration import register
print("Register")
register(
    id='gym_examples/GridWorld-v0',
    entry_point='gym_examples.envs:Grid',
    max_episode_steps=500,
)