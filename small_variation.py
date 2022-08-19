import numpy as np
from random import randrange


class SmallVariation:
    def __init__(self, pm_row_count, pm_col_count, x_count, u_count,
                 q_count, sv_mat_row_count, func_count, u_min, u_max):
        self.pm_row_count = pm_row_count
        self.pm_col_count = pm_col_count
        self.x_count = x_count
        self.u_count = u_count
        self.q_count = q_count
        self.sv_mat_row_count = sv_mat_row_count

        self.func_count = func_count
        self.A_size = x_count + q_count + pm_row_count
        self.u_min = u_min
        self.u_max = u_max

    def encode(self, pm_permitted_rows, pm_permitted_cols):
        sv_row = np.zeros(3, dtype=int)
        pm_row_index = pm_permitted_rows[randrange(len(pm_permitted_rows))]
        pm_col_index = pm_permitted_cols[randrange(len(pm_permitted_cols))]

        sv_row[0] = pm_row_index
        sv_row[1] = pm_col_index

        pm_row_index -= 1
        pm_col_index -= 1

        if pm_col_index == 0:
            new_func_index = randrange(0, self.func_count)
            sv_row[2] = new_func_index + 1
        elif pm_col_index == self.pm_col_count-1:
            new_save_index = randrange(self.x_count + self.q_count, self.A_size)
            sv_row[2] = new_save_index + 1
        elif 0 < pm_col_index < self.pm_col_count-1:
            new_arg_index = randrange(0, self.x_count + self.q_count + pm_row_index)
            sv_row[2] = new_arg_index + 1
        else:
            print('wrong col index in encode_sv', pm_col_index)
            assert False
        return sv_row
