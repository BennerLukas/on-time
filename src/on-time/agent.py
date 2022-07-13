import gym  # openAi gym
import numpy as np
import time
from IPython.display import clear_output

seed = 123
np.random.seed(seed)


class Agent:
    def __init__(self, env, obs_space_shape, action_space_shape):
        self.env = env
        self.obs_space_shape = obs_space_shape
        self.action_space_shape = action_space_shape

    def brute_force(self):
        self.env.reset()
        state, reward, done, info = None, None, None, None

        for _ in range(100):
            action = self.env.action_space.sample()
            state, reward, done, info = self.env.step(action)
            print(f"Reward: {reward}, Done: {done}, Delay: {info['average_delay']}")
            if done is True:
                break
        return state, reward, done, info

    # Train agent to find path using Reinforcement Learning
    def train_agent(self):
        q_table = np.zeros([5, 7, 7])
        # Weiche x Weichenstellung x Zugpositionen
        # Hyper-parameters
        # Learning rate
        alpha = 0.1
        # Discount factor: importance to future rewards
        gamma = 0.6
        # Exploration rate
        epsilon = 0.1

        # For plotting metrics
        all_epochs = []
        all_penalties = []

        for i in range(1, 100001):
            state = self.env.reset()

            epochs, penalties, reward, = 0, 0, 0
            done = False

            while not done:
                if np.random.uniform(0, 1) < epsilon:
                    action = self.env.action_space.sample()  # Explore action space
                else:
                    action = np.argmax(q_table[state])  # Exploit learned values

                next_state, reward, done, info = self.env.world_step(action)

                #           Q-Learning
                old_value = q_table[state, action]
                next_max = np.max(q_table[next_state])

                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                q_table[state, action] = new_value

                if reward == -10:
                    penalties += 1

                state = next_state
                epochs += 1

            if i % 100 == 0:
                clear_output(wait=True)
                print(f"Episode: {i}")

        print("Training finished.\n")
        return q_table

    # Run agent trained using Reinforcemnt learning
    def run_agent(self, state, q_table):
        epochs = 0
        penalties, reward = 0, 0
        self.env.s = state

        frames = []  # for animation
        # initial state
        frames.append({
            'frame': self.env.render(mode='ansi'),
            'state': state,
            'action': '--',
            'reward': '--'
        }
        )
        done = False

        while not done:
            # Next action is choosen from q_table
            action = np.argmax(q_table[state])
            state, reward, done, info = self.env.world_step(action)
            if reward == -10:
                penalties += 1
            # Put each rendered frame into dict for animation
            frames.append({
                'frame': self.env.render(mode='ansi'),
                'state': state,
                'action': action,
                'reward': reward
            }
            )
            epochs += 1
        return frames, epochs, penalties
