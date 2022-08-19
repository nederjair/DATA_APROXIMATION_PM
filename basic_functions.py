import numpy as np


# basic functions
def clamp(value, min_value, max_value):
    if value > max_value:
        return max_value
    elif value < min_value:
        return min_value
    else:
        return value


def exponential(z):
    max_value = 50
    min_value = -5000
    z_temp = clamp(z, min_value, max_value)
    return np.exp(z_temp)


def nat_log(z):
    if z > 0:
        return np.log(z)
    else:
        return 0


def square(z):
    max_value = 1.0e5
    min_value = -1.0e5
    z_temp = clamp(z, min_value, max_value)
    return z_temp ** 2


def square_root(z):
    if z >= 0:
        return np.sqrt(z)
    else:
        return 0


def cube(z):
    max_value = 1.0e5
    min_value = -1.0e5
    z_temp = clamp(z, min_value, max_value)
    return z_temp ** 3


def cubic_root(z):
    return np.cbrt(z)


def sign(z):
    if z < 0:
        return -1
    else:
        return 1


def sigmoid(z):
    return 1 / (1 + exponential(-1 * z))


def heaviside(z):
    if z >= 0:
        return 1
    else:
        return 0


def fun16(z):
    if np.abs(z) < 1:
        return z
    else:
        return sign(z)


def fun25(z):
    if z > 0:
        return 1
    else:
        return 0


def fun26(z):
    epsilon = 0.01
    if abs(z) < epsilon:
        return 0.0
    else:
        return sign(z)


def mult(z1, z2):
    max_value = 1.0e9
    min_value = -1.0e9
    z1_temp = clamp(z1, min_value, max_value)
    z2_temp = clamp(z2, min_value, max_value)
    return z1_temp * z2_temp


def add(z1, z2):
    max_value = 1.0e9
    min_value = -1.0e9
    z1_temp = clamp(z1, min_value, max_value)
    z2_temp = clamp(z2, min_value, max_value)
    return z1_temp + z2_temp


def div(z1, z2):
    max_value = 1.0e-5
    min_value = -1.0e-5
    if min_value < z2 < max_value:
        if z2 < 0:
            z2_temp = min_value
        else:
            z2_temp = max_value
    else:
        z2_temp = z2
    return z1 / z2_temp


def fun37(z1, z2, z3):
    if z1 > 0:
        return z2
    else:
        return z3


def fun38(z1, z2, z3):
    if z1 > z2:
        return z3
    else:
        return -z3


def fun39(z1, z2, z3):
    if z1 > 0:
        return z2 + z3
    else:
        return z2 - z3


# basic symbolic functions
def s_exponential(z):
    return 'exp('+z+')'


def s_nat_log(z):
    return 'ln(|'+z+'|)'


def s_square(z):
    return '('+z+')^2'


def s_square_root(z):
    return '(|'+z+'|)^(1/2)'


def s_cube(z):
    return '('+z+')^3'


def s_cubic_root(z):
    return '('+z+')^(1/3)'


def s_sign(z):
    return 'sgn('+z+')'


def s_mult(z1, z2):
    return '('+z1+'*' + z2+')'


def s_add(z1, z2):
    return '('+z1+'+' + z2+')'


def s_div(z1, z2):
    return '('+z1 + '/' + z2 + ')'
