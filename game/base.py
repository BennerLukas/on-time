import random
import time
from abc import ABC
from collections import deque
from typing import Tuple, Union, Optional

import gym
import numpy as np
from gym import spaces
from gym.core import ObsType, ActType

from helper import Switch, Signal, Stop
from train import Train
import sys


# TODO: Signal-Cluster (Kreuzungen) --> Observation Space: Signal-Cluster 1: {1: 5, 2: -1, 3: None}
#                                      Action Space: Signal-Cluster 1: [1,2] => 1: Signal oben grün, Signal rechts rot

class Grid(gym.Env, ABC):
    """The schematic of Mannheim's central metro system. It is simplified into a gridworld and slightly altered."""

    def __init__(self):
        """
        Initializes all grid components with automatically generated components. Also sets the world steps to 0 as
        initial value.
        """
        super(Grid, self).__init__()
        # Grid components
        self.grid = None
        self.train_grid = None
        self.step = 0
        self._init_grid()

        # Gym specific variables
        self.state = dict
        self.action_space = spaces.MultiDiscrete([5, 5, 4, 4, 4, 4, 3])
        self.observation_space = spaces.Dict({"signal_cluster_kubruecke": spaces.Box(low=-2, high=20,
                                                                                     shape=(4,), dtype=np.float32),
                                              "signal_cluster_paradeplatz": spaces.Box(low=-2, high=20,
                                                                                       shape=(4,), dtype=np.float32),
                                              "signal_cluster_handelshafen": spaces.Box(low=-2, high=20,
                                                                                        shape=(3,), dtype=np.float32),
                                              "signal_cluster_nationaltheater": spaces.Box(low=-2, high=20,
                                                                                           shape=(3,),dtype=np.float32),
                                              "signal_cluster_tattersall": spaces.Box(low=-2, high=20,
                                                                                      shape=(3,), dtype=np.float32),
                                              "signal_cluster_kabruecke": spaces.Box(low=-2, high=20,
                                                                                     shape=(3,), dtype=np.float32),
                                              "signal_cluster_wasserturm": spaces.Box(low=-2, high=20,
                                                                                      shape=(2,), dtype=np.float32)})

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, dict]:
        # TODO: Convert Actions to Signal-Changes
        # TODO: Create Observation from self.grid
        self._add_lines()
        reward = self._update_world()
        obs_state = self._convert_to_observation_space()
        if self.step > 400:
            done = True
        else:
            done = False
        avrg_delay = self._return_average_delay()

        return obs_state, reward, done, avrg_delay

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            return_info: bool = False,
            options: Optional[dict] = None,
    ) -> Union[ObsType, tuple[ObsType, dict]]:
        # TODO: Call Conversion for Observation
        self._init_grid()
        obs_state = self._convert_to_observation_space()
        return obs_state

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        # TODO @Paula für Idee wie ich es erzeuge siehe unten __str__
        pass

    def add_train_to_grid(self, x: int, y: int, train: Train):
        """
        Adds a train based on initial coordinates into the world by adding it to the train_grid. It has no logic to check
        if a train already occupies the coordinate.
        :param x: integer between 0 and the length of a grid row
        :param y: integer between 0 and the height of the grid
        :param train: train object that is to be placed
        :return: current grid step
        """
        self.train_grid[y][x] = train
        return self.step

    def _return_average_delay(self):
        delay = 0
        amount_trains = 0
        for row in self.train_grid:
            for col in row:
                if type(col) == Train:
                    delay += col.delay
                    amount_trains += 1

        delay = (delay / amount_trains) if amount_trains else 0

        return {"average_delay": delay}

    def _convert_to_observation_space(self):
        # Get delays at signal cluster 1 (Kurpfalzbrücke)
        # Northern signal
        if type(self.train_grid[0][19]) == Train:
            delay1 = self.train_grid[0][19].delay
        else:
            delay1 = None
        # Southern signal
        if type(self.train_grid[7][20]) == Train:
            delay2 = self.train_grid[7][20].delay
        else:
            delay2 = None
        # Western signal
        if type(self.train_grid[4][17]) == Train:
            delay3 = self.train_grid[4][17].delay
        else:
            delay3 = None
        # Eastern signal
        if type(self.train_grid[3][21]) == Train:
            delay4 = self.train_grid[3][21].delay
        else:
            delay4 = None
        self.state["signal_cluster_kubruecke"] = np.array([delay1, delay2, delay3, delay4], dtype=np.float32)

        # Get delays at signal cluster 2 (Paradeplatz)
        # Northern Signal
        if type(self.train_grid[8][19]) == Train:
            delay1 = self.train_grid[9][19].delay
        else:
            delay1 = None
        # Southern signal
        if type(self.train_grid[12][20]) == Train:
            delay2 = self.train_grid[7][20].delay
        else:
            delay2 = None
        # Western signal
        if type(self.train_grid[11][18]) == Train:
            delay3 = self.train_grid[4][18].delay
        else:
            delay3 = None
        # Eastern signal
        if type(self.train_grid[10][22]) == Train:
            delay4 = self.train_grid[3][22].delay
        else:
            delay4 = None
        self.state["signal_cluster_paradeplatz"] = np.array([delay1, delay2, delay3, delay4], dtype=np.float32)

        # Get delays at signal cluster 3 (Handelshafen)
        # Northern Signal
        if type(self.train_grid[9][2]) == Train:
            delay1 = self.train_grid[9][2].delay
        else:
            delay1 = None
        # Western signal
        if type(self.train_grid[11][1]) == Train:
            delay2 = self.train_grid[11][1].delay
        else:
            delay2 = None
        # Eastern signal
        if type(self.train_grid[10][5]) == Train:
            delay3 = self.train_grid[10][5].delay
        else:
            delay3 = None
        self.state["signal_cluster_handelshafen"] = np.array([delay1, delay2, delay3], dtype=np.float32)

        # Get delays at signal cluster 4 (Nationaltheater)
        # Northern Signal
        if type(self.train_grid[6][32]) == Train:
            delay1 = self.train_grid[6][32].delay
        else:
            delay1 = None
        # Southern signal
        if type(self.train_grid[10][33]) == Train:
            delay2 = self.train_grid[10][33].delay
        else:
            delay2 = None
        # Eastern signal
        if type(self.train_grid[7][35]) == Train:
            delay3 = self.train_grid[7][35].delay
        else:
            delay3 = None
        self.state["signal_cluster_nationaltheater"] = np.array([delay1, delay2, delay3], dtype=np.float32)

        # Get delays at signal cluster 5 (Tattersall)
        # Northern Signal
        if type(self.train_grid[12][32]) == Train:
            delay1 = self.train_grid[12][32].delay
        else:
            delay1 = None
        # Southern signal
        if type(self.train_grid[16][33]) == Train:
            delay2 = self.train_grid[16][33].delay
        else:
            delay2 = None
        # Eastern signal
        if type(self.train_grid[13][35]) == Train:
            delay3 = self.train_grid[13][35].delay
        else:
            delay3 = None
        self.state["signal_cluster_tattersall"] = np.array([delay1, delay2, delay3], dtype=np.float32)

        # Get delays at signal cluster 6 (Konrad-Adenauer-Brücke)
        # Southern signal
        if type(self.train_grid[22][23]) == Train:
            delay1 = self.train_grid[22][23].delay
        else:
            delay1 = None
        # Western signal
        if type(self.train_grid[20][20]) == Train:
            delay2 = self.train_grid[20][20].delay
        else:
            delay2 = None
        # Eastern signal
        if type(self.train_grid[19][24]) == Train:
            delay3 = self.train_grid[19][24].delay
        else:
            delay3 = None
        self.state["signal_cluster_kabruecke"] = np.array([delay1, delay2, delay3], dtype=np.float32)

        # Get delays at signal cluster 7 (Wasserturm)
        # Southern signal
        if type(self.train_grid[12][34]) == Train:
            delay1 = self.train_grid[12][34].delay
        else:
            delay1 = None
        # Western signal
        if type(self.train_grid[20][32]) == Train:
            delay2 = self.train_grid[20][32].delay
        else:
            delay2 = None
        self.state["signal_cluster_wasserturm"] = np.array([delay1, delay2], dtype=np.float32)
        return self.state

    def _init_grid(self):
        """
        Sets all grids to their respective default.

        :param: grid
        The grid is defined as a 2-dimensional list of element.
        A empty spot where no tracks exist is represented as 0. Vertical tracks - allowing vertical travel are
        represented by the string |.
        Horizontal tracks are given by '-'. Diagonal travel is represented by either \\ or /.
        Signals, stops and switches are integrated as objects of their respective data types.

        :param: train_grid
        The train grid is used to track the individual train objects on their path through the tracks. It has to be off
        the same dimensionality as the default grid.

        :return: None
        """
        self.grid = [  # Ausfahrt Kurpfalzbrücke
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Switch('/', '|'), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, '/', '-', '-', Stop(""), '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-',
             '|', Switch('/', '|'), Signal(), '-', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-', 0, 0, 0, 0, 0,
             0, 0],
            [0, 0, '|', 0, '-', '-', Stop(""), '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', Signal(),
             Switch('/', '-'), '|', '|', '-', '-', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '\\', '\\',
             0, 0, 0, 0, 0, 0],
            [0, 0, '|', '/', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Switch("/", "|"), 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, '\\', '\\', 0, 0, 0, 0, 0],
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Signal(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, Signal(), '\\', 0, 0, 0, 0],
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, Switch('\\', '|'), Switch('/', '|'), Switch('\\', '-'), Signal(), '-', '-'],  # Ausfahrt Nationaltheater
            [0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, '|', '|', '-', '-', '-', '-'],  # Ausfahrt Nationaltheater
            [0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Signal(), '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, Switch('/', '|'), Switch('/', '|'), 0, 0, 0, 0],
            ['-', '-', Switch('\\', '-'), '-', Switch('\\', '-'), Signal(), '-', Stop(""), '-', '-', '-', Stop(""), '-',
             '-', '-', '-', '-', '-', '-', Switch('\\', '|'), '|', Switch('\\', '-'), Signal(), '-', Stop(""), '-', '-',
             '-', '-', '-', '-', Stop(""), '-', '-', '|', Signal(), 0, 0, 0, 0],  # Ausfahrt Handelshafen
            ['-', Signal(), '-', '-', '-', '-', '-', Stop(""), '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-',
             Signal(), '|', '|', '-', '-', '-', Stop(""), '-', '-', '-', '-', '-', '-', Stop(""), Signal(),
             Switch("\\", "-"), Switch('/', '|'),
             Switch('\\', '|'), 0, 0, 0, 0],  # Ausfahrt Handelshafen
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Signal(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, Signal(), Signal(), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             Switch('\\', '|'), Switch('/', '|'), Switch('\\', '-'), Signal(), Stop(""), '-'],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', '|', '-', '-', Stop(""), '-'],  # Ausfahrt Tattersall
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', Switch('/', '|'), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', Signal(), 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '|', '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             '/', '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '\\', 0, '\\', '-', '-', Switch('/', '-'),
             Signal(), '-', Stop(""), '-', '-', '-', '-', '-', Stop(""), 0, '|', 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '-', Signal(), Switch('\\', '-'), '-',
             Switch('\\', '-'), '-', '-', Stop(""), '-', '-', '-', '-', '-', Stop(""), '/', 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', Switch('/', '-'), 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Stop(""), Signal(), 0, 0, 0, 0, 0, 0,
             0,
             0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '|', '|', 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0]
        ]
        self.train_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0]
        ]

    def _update_train(self, *args):
        """
        Recursive function to update all subsequent trains. It checks if there is a train object on the proposed new
        coordinate, and it already moved on this grid step. If it hasn't moved the function update_train is called for
        this train. The exit conditions are either there being no train on the track segment where the original train
        object wants to move to or the train on the tile "ahead" already moved this step.
        :param args: new x & y value of the train, the calculated reward in move function and the train object
        :return: float reward
        """

        if type(args[0]) == tuple:
            # list unpacking of args
            new_x, new_y, new_direction, reward, tile = args[0]
        else:
            new_x, new_y, new_direction, reward, tile = args[0].read_track()

        # check if train goes out-of-bounds and deletes it
        if new_x > 39 or new_x < 0 or new_y < 0 or new_y > 23:
            # remove train from train_grid
            tile.grid.train_grid[tile.y][tile.x] = 0
            # delete train object
            del tile
            return reward
        else:
            # calculates the new position of the train
            expected_new_tile = self.train_grid[new_y][new_x]

        # check which condition applies to the new position
        # Condition 1: Train on new position that hasn't moved on this step
        if type(expected_new_tile) == Train and expected_new_tile.step != self.step:
            # recursive call for the train on new position
            reward += self._update_train(expected_new_tile)
            # move the original out of recursion train
            expected_new_tile.move(new_x, new_y, new_direction)
            return reward
        # Condition 2: Train on new position that has already moved this step
        elif type(expected_new_tile) == Train and expected_new_tile.step == self.step:
            return reward - 1
        # Condition 3: Nothing on the new position
        else:
            tile.move(new_x, new_y, new_direction)
            return reward + 0

    def _update_world(self):
        self.step += 1
        reward = 0
        for row in self.train_grid:
            for tile in row:
                if type(tile) == Train and tile.step != self.step:
                    reward = 0 + self._update_train(tile.read_track())
        return reward

    def _update_signal(self, action_list):
        """

        :param action_list: list of 7 integers
        :return:
        """
        # Get delays at signal cluster 1 (Kurpfalzbrücke)
        # Northern signal
        delay1 = self.grid[0][19].delay
        # Southern signal
        delay2 = self.grid[7][20].delay
        # Western signal
        delay3 = self.grid[4][17].delay
        # Eastern signal
        delay4 = self.grid[3][21].delay

        # Get delays at signal cluster 2 (Paradeplatz)
        # Northern Signal
        delay1 = self.grid[9][19].delay
        # Southern signal
        delay2 = self.grid[7][20].delay
        # Western signal
        delay3 = self.grid[4][18].delay
        # Eastern signal
        delay4 = self.grid[3][22].delay

        # Get delays at signal cluster 3 (Handelshafen)
        # Northern Signal
        delay1 = self.grid[9][2].delay
        # Western signal
        delay2 = self.grid[11][1].delay
        # Eastern signal
        delay3 = self.grid[10][5].delay

        # Get delays at signal cluster 4 (Nationaltheater)
        # Northern Signal
        delay1 = self.grid[6][32].delay
        # Southern signal
        delay2 = self.grid[10][33].delay
        # Eastern signal
        delay3 = self.grid[7][35].delay

        # Get delays at signal cluster 5 (Tattersall)
        # Northern Signal
        delay1 = self.grid[12][32].delay
        # Southern signal
        delay2 = self.grid[16][33].delay
        # Eastern signal
        delay3 = self.grid[13][35].delay

        # Get delays at signal cluster 6 (Konrad-Adenauer-Brücke)
        # Southern signal
        delay1 = self.grid[22][23].delay
        # Western signal
        delay2 = self.grid[20][20].delay
        # Eastern signal
        delay3 = self.grid[19][24].delay

        # Get delays at signal cluster 7 (Wasserturm)
        # Southern signal
        self.grid[12][34]
        # Western signal
        self.grid[20][32]

        return None


    def _create_line(self, line_number: int, reverse: bool):
        """
        Creates a train line based on the line number and its tracking direction.
        :param line_number:
        :param reverse:
        :param grid:
        :return:
        """
        delay = random.randint(-3, 3)
        if line_number == 1:
            if reverse is False:
                # from TAT
                switches = deque(["-", "/", "-", "|", "|"])
                line = Train(start_x=39, start_y=13, direction="<", grid=self, switches=switches, delay=delay, line=1)
            else:
                # from KUB
                switches = deque(["|", "|", "-", "-", "/"])
                line = Train(start_x=19, start_y=0, direction="v", grid=self, switches=switches, delay=delay, line=1)

        elif line_number == 2:
            if reverse is False:
                # from NAT
                switches = deque(["-", "/", "/", "-", "-", "\\", "/"])
                line = Train(start_x=39, start_y=8, direction="<", grid=self, switches=switches, delay=delay, line=2)
            else:
                # from KUB
                switches = deque(["/", "\\", "-", "/", "/"])
                line = Train(start_x=19, start_y=0, direction="v", grid=self, switches=switches, delay=delay, line=2)

        # Line 3 skipped because of grid architecture

        elif line_number == 4:
            if reverse is False:
                # from KAB
                switches = deque(["/", "|", "|", "\\", "\\", "|", "|"])
                line = Train(start_x=24, start_y=23, direction="^", grid=self, switches=switches, delay=delay, line=4)
            else:
                # from KUB
                switches = deque(["|", "|", "\\"])
                line = Train(start_x=19, start_y=0, direction="v", grid=self, switches=switches, delay=delay, line=4)

        elif line_number == 5:
            if reverse is False:
                # from KUB
                switches = deque(["|", "|", "|", "-", "-", "|", "|", "|", "/"])
                line = Train(start_x=19, start_y=0, direction="v", grid=self, switches=switches, delay=delay, line=5)
            else:
                # from NAT
                switches = deque(["-", "/", "|", "|", "|", "-", "|"])
                line = Train(start_x=39, start_y=8, direction="<", grid=self, switches=switches, delay=delay, line=5)

        elif line_number == 6:
            if reverse is False:
                # from TAT
                switches = deque(["\\", "\\", "-", "|", "-", "-", "-"])
                line = Train(start_x=39, start_y=13, direction="<", grid=self, switches=switches, delay=delay, line=6)
            else:
                # from HHF
                switches = deque(["\\", "\\"])
                line = Train(start_x=0, start_y=11, direction=">", grid=self, switches=switches, delay=delay, line=6)

        elif line_number == 7:
            if reverse is False:
                # from NAT
                switches = deque(["\\", "/", "|", "|", "\\"])
                line = Train(start_x=39, start_y=8, direction="<", grid=self, switches=switches, delay=delay, line=7)
            else:
                # from KAB
                switches = deque(["|", "\\", "/", "\\"])
                line = Train(start_x=24, start_y=23, direction="^", grid=self, switches=switches, delay=delay, line=7)

        else:
            raise NotImplemented("Line number is not implemented! Only lines 1,2,4,5,6,7 are implemented.")

        return line

    def _add_lines(self):
        if self.step % 20 == 0:
            pass
    
        elif self.step % 20 == 1:
            self._create_line(6, False)
    
        elif self.step % 20 == 2:
            self._create_line(4, False)
            self._create_line(4, True)
    
        elif self.step % 20 == 3:
            self._create_line(1, True)
    
        elif self.step % 20 == 4:
            self._create_line(1, False)
        
        elif self.step % 20 == 5:
            self._create_line(5, True)
        
        elif self.step % 20 == 8:
            self._create_line(2, True)
            self._create_line(7, True)
    
        elif self.step % 20 == 9:
            self._create_line(6, True)
            self._create_line(5, False)
            
    def __str__(self):
        """
        Alternative print function to enable a proper view into the grid world.
        :return: fancy output string
        """
        output = ""
        # iterate over all rows
        for y, row in enumerate(self.grid):
            # iterate over all elements in the row
            for x, col in enumerate(row):
                # if there is no train on the grid coordinate look into the normal grid
                if self.train_grid[y][x] == 0:
                    if col == 0:
                        output += "  "
                    elif col in ["-", "|", "/"]:
                        output += 2 * col
                    elif col == "\\":
                        output += col * 2
                    elif type(col) == Signal:
                        output += "S" + str(col.status)
                    elif type(col) == Switch:
                        output += "W" + col.status_switched
                    elif type(col) == Stop:
                        output += "SP"  # col.name[:2]
                # if there is a train on this grid coordinate print the train instead
                else:
                    output += str(self.train_grid[y][x].line_number) + self.train_grid[y][x].direction
            output += "\n"
        return output



if __name__ == "__main__":
    gridworld = Grid()
    trains = list()
    for i in range(80):
        step(gridworld, None)
        time.sleep(.5)
