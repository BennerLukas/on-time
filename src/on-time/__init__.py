from gym.envs.registration import register

register(
    id='on-time/base',
    entry_point='base:Grid',
    max_episode_steps=450,
)