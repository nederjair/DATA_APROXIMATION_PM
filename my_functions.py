import numpy as np

from basic_functions import add, mult, div, exponential, cube, square, sign, square_root, nat_log, heaviside, \
    cubic_root, fun16, fun25, fun26, fun37, fun38, fun39
from basic_functions import s_mult, s_add, s_div, s_exponential, s_cube, s_square, s_sign, s_square_root, s_nat_log


class MyFun:
    def __init__(self, method, s_method):
        self.method = method
        self.s_method = s_method


my_fun1 = MyFun(method=lambda z: z, s_method=lambda z: z)
my_fun2 = MyFun(method=lambda z: square(z), s_method=lambda z: s_square(z))
my_fun3 = MyFun(method=lambda z: -1 * z, s_method=lambda z: '-' + z)
my_fun4 = MyFun(method=lambda z: sign(z) * np.sqrt(np.abs(z)),
                s_method=lambda z: s_sign(z) + '*' + s_square_root('||' + z))
my_fun5 = MyFun(method=lambda z: div(1.0, z), s_method=lambda z: s_div('1', z))
my_fun6 = MyFun(method=lambda z: exponential(z), s_method=lambda z: s_exponential(z))
my_fun7 = MyFun(method=lambda z: nat_log(z), s_method=lambda z: s_nat_log(z))
my_fun8 = MyFun(method=lambda z: np.tanh(0.5*z), s_method=lambda z: 'tanh(0.5*' + z + ')')
my_fun9 = MyFun(method=lambda z: heaviside, s_method=lambda z: '1 if ' + z + '>=0; 0 else')
my_fun10 = MyFun(method=lambda z: sign(z), s_method=lambda z: s_sign(z))
my_fun11 = MyFun(method=lambda z: np.cos(z), s_method=lambda z: 'cos('+z+')')
my_fun12 = MyFun(method=lambda z: np.sin(z), s_method=lambda z: 'sin('+z+')')
my_fun13 = MyFun(method=lambda z: np.arctan(z), s_method=lambda z: 'arctan('+z+')')
my_fun14 = MyFun(method=lambda z: cube(z), s_method=lambda z: s_cube(z))
my_fun15 = MyFun(method=lambda z: cubic_root(z), s_method=lambda z: '('+z+')^(1/3)')
my_fun16 = MyFun(method=lambda z: fun16(z), s_method=lambda z: z + ' if |' + z + '|<1; sgn(' + z + ')  else')
my_fun17 = MyFun(method=lambda z: mult(sign(z), nat_log(np.abs(z)+1.0)),
                 s_method=lambda z: s_sign(z) + '*' + s_nat_log(z + '1'))
my_fun18 = MyFun(method=lambda z:  mult(sign(z), exponential(np.abs(z)) - 1.0),
                 s_method=lambda z: s_mult(s_sign(z), s_exponential('|' + z + '|)-1')))
my_fun19 = MyFun(method=lambda z: mult(sign(z), exponential(-np.abs(z))),
                 s_method=lambda z: s_mult(s_sign(z), s_exponential('-|' + z + '|)')))
my_fun20 = MyFun(method=lambda z: 0.5*z, s_method=lambda z: z + '/2')
my_fun21 = MyFun(method=lambda z: 2.0*z, s_method=lambda z: '2*' + z)
my_fun22 = MyFun(method=lambda z: 1.0 - exponential(-abs(z)), s_method=lambda z: '1-' + s_exponential('|' + z + '|'))
my_fun23 = MyFun(method=lambda z: z - cube(z), s_method=lambda z: z + '-' + s_cube(z))
my_fun24 = MyFun(method=lambda z: div(1.0, 1.0 + exponential(-z)),
                 s_method=lambda z: s_div('1', '1+' + s_exponential('-' + z)))
my_fun25 = MyFun(method=lambda z: fun25(z), s_method=lambda z: '1 if ' + z + '>0; 0 else')
my_fun26 = MyFun(method=lambda z: fun26(z), s_method=lambda z: '0 if |' + z + '|<epsilon; sign(' + z + ') else')
my_fun27 = MyFun(method=lambda z: sign(z)*(1.0-square_root(1.0-square(z))),
                 s_method=lambda z: s_mult(s_sign(z), ('1-' + s_square_root('1-' + s_square(z)))))
my_fun28 = MyFun(method=lambda z: mult(z, 1.0 - exponential(-square(z))),
                 s_method=lambda z: s_mult(z, '1-'+s_exponential('-' + s_square(z))))

my_fun29 = MyFun(method=lambda z1, z2: add(z1, z2),
                 s_method=lambda z1, z2: s_add(z1, z2))
my_fun30 = MyFun(method=lambda z1, z2: mult(z1, z2),
                 s_method=lambda z1, z2: s_mult(z1, z2))
my_fun31 = MyFun(method=lambda z1, z2: np.max([z1, z2]),
                 s_method=lambda z1, z2: 'max(' + z1 + ',' + z2 + ')')
my_fun32 = MyFun(method=lambda z1, z2: np.min([z1, z2]),
                 s_method=lambda z1, z2: 'min(' + z1 + ',' + z2 + ')')
my_fun33 = MyFun(method=lambda z1, z2: add(z1, z2) - mult(z1, z2),
                 s_method=lambda z1, z2: s_add(z1, z2) + '-' + s_mult(z1, z2))
my_fun34 = MyFun(method=lambda z1, z2: mult(sign(sum(z1, z2)), square_root(add(square(z1), square(z2)))),
                 s_method=lambda z1, z2: s_mult(s_sign(s_add(z1, z2)),
                                                s_square_root(s_add(s_square(z1), s_square(z2)))))
my_fun35 = MyFun(method=lambda z1, z2: mult(sign(sum(z1, z2)), sum(abs(z1), abs(z2))),
                 s_method=lambda z1, z2: s_mult(s_sign(s_add(z1, z2)), s_add('|' + z1 + '|', '|' + z2 + '|')))
my_fun36 = MyFun(method=lambda z1, z2: mult(sign(sum(z1, z2)), mult(abs(z1), abs(z2))),
                 s_method=lambda z1, z2: s_mult(s_sign(s_add(z1, z2)), s_mult('|' + z1 + '|', '|' + z2 + '|')))
my_fun37 = MyFun(method=lambda z1, z2, z3: fun37(z1, z2, z3),
                 s_method=lambda z1, z2, z3: z2 + ' if ' + z1 + '>0;  ' + z3 + 'else')
my_fun38 = MyFun(method=lambda z1, z2, z3: fun38(z1, z2, z3),
                 s_method=lambda z1, z2, z3: z3 + ' if ' + z1 + '>' + z2 + '; -' + z3 + ' else')
my_fun39 = MyFun(method=lambda z1, z2, z3: fun39(z1, z2, z3),
                 s_method=lambda z1, z2, z3: z2 + '+' + z3 + ' if ' + z1 + '>0;  ' + z2 + '-' + z3 + 'else')
my_fun40 = MyFun(method=lambda z1, z2, z3: np.max([z1, z2, z3]),
                 s_method=lambda z1, z2, z3: 'max([' + z1 + ',' + z2 + ',' + z3 + '])')

function_approximation_list = [
    my_fun1,
    my_fun2,
    my_fun3,
    my_fun4,
    my_fun5,
    my_fun6,
    my_fun7,
    my_fun11,
    my_fun12,
    my_fun14,
    my_fun29,
    my_fun30
]
synthesis_funtion_list = [
    my_fun1,
    my_fun2,
    my_fun3,
    my_fun4,
    my_fun5,
    my_fun6,
    my_fun7,
    my_fun8,
    my_fun9,
    my_fun10,
    my_fun11,
    my_fun12,
    my_fun13,
    my_fun14,
    my_fun15,
    my_fun16,
    my_fun17,
    my_fun18,
    my_fun19,
    my_fun20,
    my_fun21,
    my_fun22,
    my_fun23,
    my_fun24,
    my_fun25,
    my_fun26,
    my_fun27,
    my_fun28,
    my_fun29,
    my_fun30,
    my_fun31,
    my_fun32,
    my_fun33,
    my_fun34,
    my_fun35,
    my_fun36,
    my_fun37,
    my_fun38,
    my_fun39,
    my_fun40
]
