import numpy as np
from random import randrange


class SmallVariation:
    def __init__(self, pm_row_count, pm_col_count, x_count, u_count, q_count, sv_mat_row_count, func_count,
                 pm_permitted_rows, pm_permitted_cols):
        self.pm_row_count = pm_row_count
        self.pm_col_count = pm_col_count
        self.x_count = x_count
        self.u_count = u_count
        self.q_count = q_count
        self.sv_mat_row_count = sv_mat_row_count
        self.pm_permitted_rows = pm_permitted_rows
        self.pm_permitted_cols = pm_permitted_cols

        self.func_count = func_count
        self.a_size = x_count + q_count + pm_row_count

    def encode(self):
        sv_row = np.zeros(4, dtype=int)
        pm_row_index = self.pm_permitted_rows[randrange(len(self.pm_permitted_rows))]
        pm_col_index = self.pm_permitted_cols[randrange(len(self.pm_permitted_cols))]
        u_index = randrange(1, self.u_count + 1)

        sv_row[0] = u_index
        sv_row[1] = pm_row_index
        sv_row[2] = pm_col_index

        if pm_col_index == 1:
            new_func_index = randrange(0, self.func_count)
            sv_row[3] = new_func_index + 1
        elif pm_col_index == self.pm_col_count:
            new_save_index = randrange(self.x_count + self.q_count, self.a_size)
            sv_row[3] = new_save_index + 1
        elif 1 < pm_col_index < self.pm_col_count:
            new_arg_index = randrange(0, self.x_count + self.q_count + pm_row_index)
            sv_row[3] = new_arg_index + 1
        else:
            print('wrong col index in encode_sv', pm_col_index)
            assert False
        return sv_row

    def apply_one_small_variation(self, basic_solution_copy, sv_row):
        pm_u_index = sv_row[0] - 1
        pm_row_index = sv_row[1] - 1
        pm_col_index = sv_row[2] - 1
        new_value = sv_row[3]
        if -1 < pm_row_index < self.pm_row_count and -1 < pm_col_index < self.pm_col_count and new_value > -1:
            basic_solution_copy[pm_u_index][pm_row_index][pm_col_index] = new_value
        else:
            print('wrong parse matrix index')
            print('parse matrix row index = ', pm_row_index)
            print('parse matrix col index = ', pm_col_index)
            print('parse matrix new index value = ', new_value)
        return basic_solution_copy
