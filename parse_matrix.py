import numpy as np
from inspect import signature
from my_functions import synthesis_function_list as function_list
from basic_functions import clamp


class PM:
    def __init__(self, pm_row_count, pm_col_count, x_count,
                 u_count, q_count, sv_mat_row_count, u_min, u_max, max_arg_count):
        self.max_arg_count = max_arg_count
        self.pm_col_count = pm_col_count
        self.pm_row_count = pm_row_count
        self.x_count = x_count
        self.q_count = q_count
        self.u_count = u_count
        self.sv_mat_row_count = sv_mat_row_count

        self.function_list = function_list
        self.function_count = len(function_list)

        self.argument_count = self.x_count + self.q_count + self.pm_row_count
        self.argument_vector = np.zeros(self.argument_count)
        self.argument_vector_symbol = ['' for _ in range(self.argument_count)]

        self.args = np.full(self.max_arg_count, np.nan)
        self.args_symbol = ['' for _ in range(self.max_arg_count)]
        self.u_min = u_min
        self.u_max = u_max

        self.basic_solution = self.encode_basic()

    def encode_basic(self):
        p_mat = np.ones((self.pm_row_count, self.pm_col_count), dtype=int)
        # multiplication index
        mult_index = 30
        # addition index
        add_index = 29
        xi_index = self.x_count + 1
        qi_index = 1
        save_index = self.x_count + self.q_count + 1
        for rowIndex in range(0, self.x_count):
            p_mat[rowIndex][0] = mult_index
            p_mat[rowIndex][1] = qi_index
            p_mat[rowIndex][2] = xi_index
            p_mat[rowIndex][-1] = save_index

            xi_index += 1
            qi_index += 1
            save_index += 1
        a1_index = self.q_count + self.x_count + 1
        a2_index = self.q_count + self.x_count + 2
        for rowIndex in range(self.x_count, 2*self.x_count-1):
            p_mat[rowIndex+self.x_count][0] = add_index
            p_mat[rowIndex+self.x_count][1] = a1_index
            p_mat[rowIndex+self.x_count][2] = a2_index
            p_mat[rowIndex+self.x_count][-1] = save_index

            a1_index = save_index
            a2_index += 1
            save_index += 1

        # neutral function index
        neutral_func_index = 1
        a1_index = save_index
        save_index += 1
        for rowIndex in range(2*self.x_count-1, self.pm_row_count):
            p_mat[rowIndex][0] = neutral_func_index
            p_mat[rowIndex][1] = a1_index
            p_mat[rowIndex][-1] = save_index

            a1_index = save_index
            save_index += 1
        return p_mat

    def decode(self, xi, q, mat):
        self.argument_vector[0:self.x_count] = xi.copy()
        self.argument_vector[self.x_count:self.x_count + self.q_count] = q.copy()
        self.argument_vector[self.x_count + self.q_count:] = 0.0

        for rowIndex in range(0, self.pm_row_count):
            function_index = mat[rowIndex][0] - 1
            save_index = mat[rowIndex][-1] - 1
            if 0 <= function_index < self.function_count and \
                    self.x_count + self.q_count <= save_index < self.x_count + self.q_count + self.pm_row_count:
                func = self.function_list[function_index].method
                func_arg_count = len(signature(func).parameters)
                for col_index in range(1, func_arg_count + 1):
                    arg_index = mat[rowIndex][col_index] - 1
                    if 0 <= arg_index < self.argument_count:
                        current_arg = self.argument_vector[arg_index]
                    else:
                        print('bad argument index')
                        print('argument index = ', arg_index)
                        print('argument index limits = [0, ' + str(self.argument_count) + ']')
                        assert False
                    self.args[col_index - 1] = current_arg
                result = func(*self.args[0:func_arg_count])
                self.argument_vector[save_index] = result
            else:
                print('bad function or save index')
                print('function index = ', function_index)
                print('save index = ', save_index)
                print('function index limits : [0, ' + str(self.function_count) + ']')
                print('permitted save index: [' + str(self.x_count + self.q_count) +
                      ', ' + str(self.argument_count) + ']')
                assert False
        self.argument_vector[-1] = clamp(self.argument_vector[-1], self.u_min, self.u_max)
        return self.argument_vector[-1]

    def decode_symbol(self, q, mat):
        self.argument_vector_symbol = ['0' for _ in range(self.argument_count)]
        self.argument_vector_symbol[0:self.x_count] = ['x' + str(k + 1) for k in range(self.x_count)]
        self.argument_vector_symbol[self.x_count:self.x_count + self.q_count] = \
            [str(round(q[k], 3)) for k in range(self.q_count)]

        for rowIndex in range(0, self.pm_row_count):
            function_index = mat[rowIndex][0] - 1
            save_index = mat[rowIndex][-1] - 1
            if 0 <= function_index < self.function_count and \
                    self.x_count + self.q_count <= save_index < self.x_count + self.q_count + self.pm_row_count:
                func = self.function_list[function_index].s_method
                func_arg_count = len(signature(func).parameters)
                for col_index in range(1, func_arg_count + 1):
                    arg_index = mat[rowIndex][col_index] - 1
                    if 0 <= arg_index < self.argument_count:
                        current_arg = self.argument_vector_symbol[arg_index]
                    else:
                        print('bad argument index')
                        print('argument index = ', arg_index)
                        print('argument index limits = [0, ' + str(self.argument_count) + ']')
                        assert False
                    self.args_symbol[col_index - 1] = current_arg
                result = func(*self.args_symbol[0:func_arg_count])
                self.argument_vector_symbol[save_index] = result
            else:
                print('\nbad function or save index')
                print('function index = ', function_index)
                print('save index = ', save_index)
                print('function index limits : [0, ' + str(self.function_count) + ']')
                print('permitted save index: [' + str(self.x_count + self.q_count) +
                      ', ' + str(self.argument_count) + ']')
                assert False
        return self.argument_vector_symbol[-1]
