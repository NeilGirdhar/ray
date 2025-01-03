# __rllib-custom-gym-env-begin__
import gymnasium as gym
import numpy as np

import ray
from ray.rllib.algorithms.ppo import PPOConfig


class SimpleCorridor(gym.Env):
    def __init__(self, config):
        self.end_pos = config["corridor_length"]
        self.cur_pos = 0.0
        self.action_space = gym.spaces.Discrete(2)  # right/left
        self.observation_space = gym.spaces.Box(0.0, self.end_pos, shape=(1,))

    def reset(self, *, seed=None, options=None):
        self.cur_pos = 0.0
        return np.array([self.cur_pos]), {}

    def step(self, action):
        if action == 0 and self.cur_pos > 0.0:  # move right (towards goal)
            self.cur_pos -= 1.0
        elif action == 1:  # move left (towards start)
            self.cur_pos += 1.0
        if self.cur_pos >= self.end_pos:
            return np.array([0.0]), 1.0, True, True, {}
        else:
            return np.array([self.cur_pos]), -0.1, False, False, {}


ray.init()

config = PPOConfig().environment(SimpleCorridor, env_config={"corridor_length": 5})
algo = config.build()

for _ in range(3):
    print(algo.train())

algo.stop()
# __rllib-custom-gym-env-end__
