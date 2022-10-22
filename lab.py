# from my_functions import synthesis_function_list
import shelve
from pathlib import Path

import numpy as np

'''space = 10
x_count = 3
q_count = 7
u_count = 2
max_arg_count = 3
pm_row_count = 2*x_count - 1 + space
pm_col_count = 1 + max_arg_count + 1
sv_mat_row_count = q_count + 3*x_count + space - 1
u_min = -10
u_max = 10
q_min = 0
q_max = 10
func_count = len(synthesis_function_list)
pm_permitted_rows = [i for i in range(2*x_count, pm_row_count)]
pm_permitted_cols = [1, 2, 3, 4]'''
current_path = Path.cwd()
live_reg_data_folder_path = current_path / Path('history_regression_data')
history_data_folder_path = current_path / Path('live_regression_data')
optimization_data_folder_path = current_path / Path('optimization')

reg_shelf_file_path = optimization_data_folder_path / Path('plot_x0_' + str(0))
reg_shelf_file = shelve.open(str(reg_shelf_file_path))
x_data_array = reg_shelf_file['x_data_array'][0]
u_data_array = reg_shelf_file['u_data_array'][0]
# x0 = reg_shelf_file['x0']
reg_shelf_file.close()
print(type(u_data_array))
print(u_data_array.shape)

for x0_index in range(1, 4):
    reg_shelf_file_path = optimization_data_folder_path / Path('plot_x0_' + str(x0_index))
    reg_shelf_file = shelve.open(str(reg_shelf_file_path))

    x_data_array = np.concatenate((x_data_array, reg_shelf_file['x_data_array'][0]), axis=1)
    u_data_array = np.concatenate((u_data_array, reg_shelf_file['u_data_array'][0]), axis=1)
    # x0 = np.concatenate((x0, reg_shelf_file['x0']), axis=None)
    reg_shelf_file.close()

print(type(u_data_array))
print(u_data_array.shape)

reg_shelf_file = shelve.open(str(optimization_data_folder_path / Path('optimization')))
reg_shelf_file['x_count'] = 3
reg_shelf_file['u_count'] = 2
reg_shelf_file['u_min'] = -10
reg_shelf_file['u_max'] = 10
reg_shelf_file['x_data'] = x_data_array
reg_shelf_file['y_target'] = u_data_array
reg_shelf_file.close()

