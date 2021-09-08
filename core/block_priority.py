from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree, Stack

from core.block_depth import BlockDepth
from core.config import PRIORITY
from core.util import *

atw_prior = AnnotatedTreeWalker('type')


def exec(ptree):
    return atw_prior(ptree)


@atw_prior.register
def atomExpr(visit, ast):
    return None


@atw_prior.register
def subExpr(visit, ast):
    return None


def arithExpr(visit, ast):
    if is_calculable(ast):
        ast.root['_calc'] = 'next'
        ast.root['priority'] = 0
        return None

    left, right = ast.children
    if left.root['priority'] >= right.root['priority']:
        par = visit(left)
    else:
        par = visit(right)

    if is_next_to_calc(left) or is_next_to_calc(right):
        return ast
    return par


@atw_prior.register
def addSubExpr(visit, ast):
    par = arithExpr(visit, ast)

    left, right = ast.children
    child_types = set(child.root['type'] for child in ast.children)

    ast.root['priority'] = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])

    if 'addSubExpr' in child_types and child_types & {'subExpr', 'atomExpr'}:
        if is_next_to_calc(left):
            del left.root['_calc']
            ast.root['_calc'] = 'next'
            ast.root['priority'] = 0
        elif is_next_to_calc(right):
            del right.root['_calc']
            ast.root['_calc'] = 'next'
            ast.root['priority'] = 0
    return par


@atw_prior.register
def divProdExpr(visit, ast):
    par = arithExpr(visit, ast)

    left, right = ast.children
    child_types = set(child.root['type'] for child in ast.children)

    if not is_next_to_calc(ast):
        ast.root['priority'] = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])

    if 'divProdExpr' in child_types and child_types & {'subExpr', 'atomExpr'}:
        if is_next_to_calc(left):
            del left.root['_calc']
            ast.root['_calc'] = 'next'
            ast.root['priority'] = 0
        elif is_next_to_calc(right):
            del right.root['_calc']
            ast.root['_calc'] = 'next'
            ast.root['priority'] = 0
    return par


@atw_prior.register
def powExpr(visit, ast):
    par = arithExpr(visit, ast)
    if not is_next_to_calc(ast):
        ast.root['priority'] = max(PRIORITY['powExpr'], ast.children[0].root['priority'])
    return par


@atw_prior.register
def unaryExpr(visit, ast):
    if is_calculable(ast):
        ast.root['_calc'] = 'next'
        return None
    par = visit(ast.children[0])
    ast.root['priority'] = max(PRIORITY['unaryExpr'], ast.children[0].root['priority'])

    if is_next_to_calc(ast.children[0]):
        return ast
    return par


@atw_prior.register
def fractExpr(visit, ast):
    par = arithExpr(visit, ast)
    if not is_next_to_calc(ast):
        ast.root['priority'] = max(PRIORITY['fractExpr'], ast.children[0].root['priority'])
    return par


def container(visit, ast):
    par = visit(ast.children[0])
    if is_next_to_calc(ast.children[0]):
        return ast
    return par


@atw_prior.register
def main(visit, ast): return container(visit, ast)


@atw_prior.register
def roundBlockExpr(visit, ast): return container(visit, ast)


@atw_prior.register
def squareBlockExpr(visit, ast): return container(visit, ast)


@atw_prior.register
def curlyBlockExpr(visit, ast): return container(visit, ast)
