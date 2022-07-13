import gym  # openAi gym
import numpy as np
import time
from IPython.display import clear_output

seed = 123
np.random.seed(seed)


class Agent:
    def __init__(self, env):
        self.env = None

    # Brute Force - only exploration
    def brute_force(self, state):
        self.env.s = state
        epochs = 0
        penalties = 0
        reward = 0
        frames = list()  # for animation
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
            # Next action is chosen randomly
            action = self.env.action_space.sample()  # chooses random possible action
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

    # Visualise frames
    def print_frames(self, frames, time_btw_frames=0.1):
        for i, frame in enumerate(frames):
            clear_output(wait=True)
            print(frame['frame'])
            print(f"Timestep: {i}")
            print(f"State: {frame['state']}")
            print(f"Action: {frame['action']}")
            print(f"Reward: {frame['reward']}")
            time.sleep(time_btw_frames)

    # Train agent to find path using Reinforcement Learning
    def train_agent(self):
        q_table = np.zeros([self.env.observation_space.n, self.env.action_space.n])
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