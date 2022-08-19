import numpy as np
from random import uniform


class Coefficients:
    def __init__(self, q_count, q_min, q_max):
        self.q_count = q_count
        self.q_min = q_min
        self.q_max = q_max

    def encode(self):
        return np.array([uniform(0, 1) * (self.q_max - self.q_min) + self.q_min for _ in range(self.q_count)])
