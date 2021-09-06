from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree, Stack

from core.block_depth import BlockDepth
from core.util import *

from operator import add, mul, truediv, sub

atw_eval = AnnotatedTreeWalker('type')

ARITH_OP = {
    '+': add,
    '-': sub,
    'x': mul,
    ':': Fraction,
    '/': Fraction
}

MEMORY = {}
def exec(ast, memory):
    global MEMORY
    MEMORY = memory
    return atw_eval(ast)

@atw_eval.register
def atomExpr(visit, ast):
    return ast.root['value']


@atw_eval.register
def subExpr(visit, ast):
    return MEMORY[ast.root['ID']].root['value']


@atw_eval.register
def addSubExpr(visit, ast):
    left, right = ast.children
    op = ast.root['op']
    left, right = visit(left), visit(right)
    return ARITH_OP[op](left, right)


@atw_eval.register
def divProdExpr(visit, ast):
    left, right = ast.children
    op = ast.root['op']
    left, right = visit(left), visit(right)
    return ARITH_OP[op](left, right)


@atw_eval.register
def powExpr(visit, ast):
    left, right = ast.children
    left, right = visit(left), visit(right)
    value = pow(left, right) if right > 0 else Fraction(1, pow(left, -right))
    return value


@atw_eval.register
def unaryExpr(visit, ast):
    value = visit(ast.children[0])
    if ast.root['op'] == '-':
        value = -value
    return value


@atw_eval.register
def fractExpr(visit, ast):
    left, right = ast.children
    left, right = visit(left), visit(right)
    return Fraction(left, right)


@atw_eval.register
def main(visit, ast):
    return visit(ast.children[0])
