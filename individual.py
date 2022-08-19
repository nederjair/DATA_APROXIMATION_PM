import numpy as np
from small_variation import SmallVariation
from coefficients import Coefficients
from parse_matrix import PM
from random import uniform


class Individual:
    def __init__(self, max_arg_count, pm_row_count, pm_col_count, x_count,
                 u_count, q_count, sv_mat_row_count, func_count,
                 u_min, u_max, q_min, q_max, pm_permitted_rows, pm_permitted_cols):

        self.small_variation_object = SmallVariation(pm_row_count, pm_col_count, x_count,
                                                     u_count, q_count, sv_mat_row_count, func_count, u_min, u_max)
        self.coefficients_object = Coefficients(q_count, q_min, q_max)
        self.pm_object = PM(pm_row_count, pm_col_count, x_count,
                            u_count, q_count, sv_mat_row_count, u_min, u_max, max_arg_count)
        self.sv_mat_row_count = sv_mat_row_count
        self.q_count = q_count
        self.q_min = q_min
        self.q_max = q_max
        self.pm_permitted_rows = pm_permitted_rows
        self.pm_permitted_cols = pm_permitted_cols
        self.pm_col_count = pm_col_count
        self.pm_row_count = pm_row_count

    def encode(self):
        sv_mat = np.zeros((self.sv_mat_row_count, 3), dtype=int)
        for k in range(self.sv_mat_row_count):
            sv_mat[k] = self.small_variation_object.encode(self.pm_permitted_rows, self.pm_permitted_cols)
        q = self.coefficients_object.encode()
        return sv_mat, q

    def calculate_y(self, sv_mat, q, target_object):
        mat = self.apply_to_basic_solution(sv_mat)
        y = np.zeros(target_object.samples)
        for sample in range(target_object.samples):
            y[sample] = self.pm_object.decode(target_object.x[:, sample], q, mat)
        return y

    def calculate_y_symbol(self, sv_mat, q):
        mat = self.apply_to_basic_solution(sv_mat)
        return self.pm_object.decode_symbol(q, mat)

    def calc_score(self, sv_mat, q, target_object):
        y = self.calculate_y(sv_mat, q, target_object)
        return np.sum(np.abs(y - target_object.y))

    def apply_to_basic_solution(self, sv_mat):
        basic_solution_temp = self.pm_object.basic_solution.copy()
        for row in range(self.sv_mat_row_count):
            pm_row_index = sv_mat[row][0] - 1
            pm_col_index = sv_mat[row][1] - 1
            new_value = sv_mat[row][2]
            if -1 < pm_row_index < self.pm_row_count and -1 < pm_col_index < self.pm_col_count and new_value > -1:
                basic_solution_temp[pm_row_index][pm_col_index] = new_value
            else:
                print('wrong parse matrix index')
                print('parse matrix row index = ', pm_row_index)
                print('parse matrix col index = ', pm_col_index)
                print('parse matrix new index value = ', new_value)
        return basic_solution_temp

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
