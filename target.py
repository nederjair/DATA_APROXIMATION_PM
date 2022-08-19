import numpy as np
from random import uniform


class Target:
    def __init__(self, x_count, x_min, x_max, samples):
        self.x_count = x_count
        self.x_min = x_min
        self.x_max = x_max
        self.samples = samples
        self.x = np.zeros((self.x_count, self.samples))
        self.y = np.zeros(self.samples)

    def randomly_generate_x(self):
        self.x = np.array([[uniform(self.x_min, self.x_max) for _ in range(self.samples)] for _ in range(self.x_count)])

    def set_y(self, y):
        self.y = y
