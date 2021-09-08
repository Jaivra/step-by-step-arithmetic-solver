from fractions import Fraction


def check_type(f):
    def check_type_aux(*x):
        res = f(*x)
        if isinstance(res, Fraction):
            return res
        if isinstance(res, float) and not res.is_integer():
            return res
        return int(res)
    return check_type_aux

@check_type
def tmp(a, b):
    return a + b

print(tmp(2.3, 3.7))