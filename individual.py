import numpy as np
from small_variation import SmallVariation
from coefficients import Coefficients
from parse_matrix import PM
from random import uniform


class Individual:
    def __init__(self, max_arg_count, pm_row_count, pm_col_count, x_count,
                 u_count, q_count, sv_mat_row_count, func_count,
                 u_min, u_max, q_min, q_max, pm_permitted_rows, pm_permitted_cols):

        self.small_variation_object = SmallVariation(pm_row_count, pm_col_count, x_count, u_count, q_count,
                                                     sv_mat_row_count, func_count, pm_permitted_rows, pm_permitted_cols)
        self.coefficients_object = Coefficients(q_count, q_min, q_max)
        self.pm_object = PM(pm_row_count, pm_col_count, x_count,
                            u_count, q_count, sv_mat_row_count, u_min, u_max, max_arg_count)
        self.sv_mat_row_count = sv_mat_row_count
        self.q_count = q_count
        self.u_count = u_count
        self.q_min = q_min
        self.q_max = q_max
        self.pm_permitted_rows = pm_permitted_rows
        self.pm_permitted_cols = pm_permitted_cols
        self.pm_col_count = pm_col_count
        self.pm_row_count = pm_row_count

    def encode_basic_solution(self):
        basic_solution_matrix = np.zeros((self.u_count, self.pm_row_count, self.pm_col_count), dtype=int)
        for k in range(self.u_count):
            basic_solution_matrix[k] = self.pm_object.encode_basic()
        return basic_solution_matrix

    def encode(self):
        sv_mat = np.zeros((self.sv_mat_row_count, 4), dtype=int)
        q_vec = self.coefficients_object.encode()
        for k in range(self.sv_mat_row_count):
            sv_mat[k] = self.small_variation_object.encode()
        return sv_mat, q_vec

    def calculate_y(self, sv_mat, q, x, samples):
        mat = self.apply_to_basic_solution(sv_mat)
        y = np.zeros((self.u_count, samples))
        for u in range(self.u_count):
            for sample in range(samples):
                y[u][sample] = self.pm_object.decode(x[:, sample], q, mat[u])
        return y

    def calculate_y_symbol(self, sv_mat, q):
        mat = self.apply_to_basic_solution(sv_mat)
        y = ['NONE' for _ in range(self.u_count)]
        for u in range(self.u_count):
            y[u] = self.pm_object.decode_symbol(q, mat[u])
        return y

    def calc_score(self, sv_mat, q, x, y_target, samples):
        y = self.calculate_y(sv_mat, q, x, samples)
        return np.sum(np.abs(y - y_target))

    def apply_to_basic_solution(self, sv_mat):
        basic_solution_copy = self.encode_basic_solution()
        for row in range(self.sv_mat_row_count):
            u_index = sv_mat[row][0] - 1
            pm_row_index = sv_mat[row][1] - 1
            pm_col_index = sv_mat[row][2] - 1
            new_value = sv_mat[row][3]
            if -1 < pm_row_index < self.pm_row_count and -1 < pm_col_index < self.pm_col_count and new_value > -1:
                basic_solution_copy[u_index][pm_row_index][pm_col_index] = new_value
            else:
                print('wrong parse matrix index')
                print('parse matrix row index = ', pm_row_index)
                print('parse matrix col index = ', pm_col_index)
                print('parse matrix new index value = ', new_value)
        return basic_solution_copy

    def mutation(self, sv_mat, q,  sv_row_index, q_index):
        sv_mat_mutated = sv_mat.copy()
        q_mutated = q.copy()
        sv_mat_mutated[sv_row_index] = \
            self.small_variation_object.encode(self.pm_permitted_rows, self.pm_permitted_cols)
        q_mutated[q_index] = uniform(0, 1) * (self.q_max - self.q_min) + self.q_min

        offsprings_sv = np.zeros((4, sv_mat.shape[0], sv_mat.shape[1]), dtype=int)
        offsprings_sv[0:2] = sv_mat.copy()
        offsprings_sv[2:4] = sv_mat_mutated.copy()

        offsprings_q = np.zeros((4, q.shape[0]))
        offsprings_q[0] = q.copy()
        offsprings_q[1] = q_mutated.copy()
        offsprings_q[2] = q.copy()
        offsprings_q[3] = q_mutated.copy()
        return offsprings_sv, offsprings_q
