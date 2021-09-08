from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree

from core.config import PRIORITY
from core.util import *

arith2ast = AnnotatedTreeWalker('name')


def exec(ptree):
    return arith2ast(ptree)

@arith2ast.register
def RAT(visit, ptree):
    return Fraction(ptree.root['value'])


@arith2ast.register
def INT(visit, ptree):
    return int(ptree.root['value'])


@arith2ast.register
def REAL(visit, ptree):
    return float(ptree.root['value'])


@arith2ast.register
def atomExpr(visit, ptree):
    if len(ptree.children) > 1:
        value = -visit(ptree.children[1])
    else:
        value = visit(ptree.children[0])
    return Tree({'type': 'atomExpr', 'value': value, 'priority': 0}, [])


@arith2ast.register
def addSubExpr(visit, ptree):
    left, op, right = ptree.children
    left = visit(left)
    right = visit(right)

    priority = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])

    return Tree({'type': 'addSubExpr', 'op': op.root['value'], 'priority': priority}, [left, right])


@arith2ast.register
def divProdExpr(visit, ptree):
    left, op, right = ptree.children
    left = visit(left)
    right = visit(right)

    priority = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])

    return Tree({'type': 'divProdExpr', 'op': op.root['value'], 'priority': priority}, [left, right])


@arith2ast.register
def powExpr(visit, ptree):
    left, _, right = ptree.children
    left = visit(left)
    right = visit(right)

    priority = max(PRIORITY['powExpr'], left.root['priority'], right.root['priority'])

    return Tree({'type': 'powExpr', 'priority': priority}, [left, right])


@arith2ast.register
def unaryExpr(visit, ptree):
    op, subexpr = ptree.children
    subexpr = visit(subexpr)

    priority = max(PRIORITY['unaryExpr'], subexpr.root['priority'])

    return Tree({'type': 'unaryExpr', 'op': op.root['value'], 'priority': priority}, [subexpr])


@arith2ast.register
def fractExpr(visit, ptree):
    left, _, right = ptree.children
    left = visit(left)
    right = visit(right)

    priority = max(PRIORITY['fractExpr'], left.root['priority'], right.root['priority'])

    return Tree({'type': 'fractExpr', 'priority': priority}, [left, right])


@arith2ast.register
def roundBlockExpr(visit, ptree):
    _, subexpr, _ = ptree.children
    subexpr = visit(subexpr)

    if is_container(subexpr) or is_atom(subexpr):
        return subexpr
    return Tree({'type': 'roundBlockExpr', 'priority': 0}, [subexpr])


@arith2ast.register
def squareBlockExpr(visit, ptree):
    _, subexpr, _ = ptree.children
    subexpr = visit(subexpr)

    if is_container(subexpr) or is_atom(subexpr):
        return subexpr
    return Tree({'type': 'squareBlockExpr', 'priority': 0}, [subexpr])


@arith2ast.register
def curlyBlockExpr(visit, ptree):
    _, subexpr, _ = ptree.children
    subexpr = visit(subexpr)

    if is_container(subexpr) or is_atom(subexpr):
        return subexpr
    return Tree({'type': 'curlyBlockExpr', 'priority': 0}, [subexpr])


@arith2ast.register
def subExpr(visit, ptree):
    _, subexpr, _ = ptree.children
    return visit(subexpr)


@arith2ast.register
def s(visit, ptree):
    expr = visit(ptree.children[0])
    return Tree({'type': 'main'}, [expr])
