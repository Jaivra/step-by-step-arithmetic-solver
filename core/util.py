from fractions import Fraction
import re

from IPython.core.display import display, Latex
from liblet import Tree


def is_container(ast):
    return ast.root['type'] in {'roundBlockExpr', 'squareBlockExpr', 'curlyBlockExpr'}


def is_atom(ast):
    return ast.root['type'] == 'atomExpr'


def display_latex(tex):
    display(Latex(fr"""\begin{{align}}{tex}\end{{align}}"""))


def is_calculable(ast):
    return all(child.root['type'] in {'atomExpr', 'subExpr'} for child in ast.children)


def is_next_to_calc(ast):
    return '_calc' in ast.root and ast.root['_calc'] == 'next'


def block2ast(main_block, memory):
    if main_block.root['type'] == 'subExpr':
        return block2ast(memory[main_block.root['ID']], memory)
    return Tree(main_block.root, [block2ast(child, memory) for child in main_block.children])


def check_type(f):
    def check_type_aux(*x):
        res = f(*x)
        if isinstance(res, Fraction) and res.denominator != 1:
            return res
        if isinstance(res, float) and not res.is_integer():
            return res  # round(res, 3)
        return int(res)

    return check_type_aux


def is_negative_number(token):
    return token[0] == '-' and (is_integer(token) or is_rational(token) or is_float(token))


def is_natural(token):
    # return re.match(r'[-|+]*\d+$', token)
    return token[0] != '-' and is_integer(token)


def is_integer(token):
    # return re.match(r'[-|+]*\d+$', token)
    return re.match(r'-?\d+$', token)


def is_rational(token):
    # return re.match(r'[-|+]*\d+(?:\.\d+)?/\d+(?:\.\d+)?$', token)
    return re.match(r'-?\d+(?:\.\d+)?/\d+(?:\.\d+)?$', token)


def is_float(token):
    # return re.match(r'-?[0-9]+\.[0-9]+$', token)
    return re.match(r'-?[0-9]+\.[0-9]+$', token)





def tokenize(expr):
    reg = r'\d+(?:\.\d+)?|[^ 0-9|\.]'
    return re.findall(reg, ''.join(expr.split()))


def create_domain_checker(domain):
    DISPATCH_DOMAIN_TABLE = {
        'N': is_natural,
        'Z': is_integer,
        'Q': lambda x: is_integer(x) or is_rational(x),
        'R': lambda x: is_integer(x) or is_rational(x) or is_float(x) or re.match(r'([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))$', x) #for scientific notation
    }
    def domain_checker(res):
        token = str(res)
        return DISPATCH_DOMAIN_TABLE[domain](token)
    return domain_checker