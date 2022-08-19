# from symbolic_regression import SymbolicRegression
# from my_functions import function_approximation_list as function_list
# import numpy as np
#
#
# def target_function(x):
#     return 0.5*np.cos(x[0]) + np.sin(x[1])
#
#
# pop_size = 100
#
# max_arg_count = 3
# pm_row_count = 15  # minimum value: 2*x_count - 1
# pm_col_count = 1 + max_arg_count + 1
# x_count = 3
# u_count = 2
# q_count = 3
# q_min = 0
# q_max = 10
# sv_mat_row_count = 10
# func_count = len(function_list)
# u_min = -10
# u_max = 10
# x_min = -4
# x_max = 4
# samples = 50
# elite_size = 5
#
# symbolic_regression = SymbolicRegression(max_arg_count, pm_row_count, x_count, u_count, q_count, q_min, q_max,
#                                          sv_mat_row_count, func_count, u_min, u_max, x_min, x_max, samples,
#                                          target_function, pop_size, elite_size)
#
# symbolic_regression.start_from_scratch(max_generations=100, reset_max_attempts=10)

from GUI import Gui
gui = Gui()
gui.root.mainloop()


