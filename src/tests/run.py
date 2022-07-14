from base import Grid

env = Grid()


def brute_force(env):
    env.reset()
    for _ in range(400):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        print(f"World Step: {env.world_step} | Reward: {reward}, Done: {done}, Delay: {info['average_delay']}")
        print(env)
        if done is True:
            break


brute_force(env)
pass