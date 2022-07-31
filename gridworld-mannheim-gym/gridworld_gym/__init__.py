from gym.envs.registration import register
print("Registered")
register(
    id="gridworld-v0",
    entry_point="gridworld_gym.envs:GridWorldEnv",
)