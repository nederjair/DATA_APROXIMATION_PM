from small_variation import SmallVariation
from my_functions import synthesis_function_list
from parse_matrix import PM
from coefficients import Coefficients
space = 10
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
pm_permitted_cols = [1, 2, 3, 4]

sv = SmallVariation(pm_row_count, pm_col_count, x_count, u_count, q_count, sv_mat_row_count, func_count, u_min, u_max)
'''option = input('do you wish to continue?')
while option == '':
    print(sv.encode(pm_permitted_rows, pm_permitted_cols))
    option = input('do you wish to continue?')

print('End.')'''


pm_obj = PM(pm_row_count, pm_col_count, x_count, u_count, q_count, sv_mat_row_count, u_min, u_max, max_arg_count)
q_obj = Coefficients(q_count, q_min, q_max)
p_mat = pm_obj.encode_basic()
q = q_obj.encode()
option = input('press enter to continue')
while option == '':
    expression = pm_obj.decode_symbol(q, p_mat)
    print(expression)
    option = input('do you wish to continue?')

print('End.')