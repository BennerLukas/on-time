from base import Grid

env = Grid()


def brute_force(env):
    env.reset()
    for _ in range(100):
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        print(f"Reward: {reward}, Done: {done}, Delay: {info['average_delay']}")
        if done is True:
            break


brute_force(env)
pass