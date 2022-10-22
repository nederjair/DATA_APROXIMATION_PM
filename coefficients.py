from random import uniform
import numpy as np


class Coefficients:
    def __init__(self, q_count, q_min, q_max):
        self.q_count = q_count
        self.q_min = q_min
        self.q_max = q_max

    def encode(self):
        q_vec = np.zeros(self.q_count)
        for k in range(self.q_count):
            q_vec[k] = uniform(0, 1) * (self.q_max - self.q_min) + self.q_min
        return q_vec
