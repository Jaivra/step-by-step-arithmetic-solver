from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree, Stack

from core.block_depth import BlockDepth
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
        return None

    left, right = ast.children
    if left.root['priority'] >= right.root['priority']:
        par = visit(left)
    else:
        par = visit(right)

    if is_next_to_calc(left) or is_next_to_calc(right):
        return ast
    else:
        return par


@atw_prior.register
def addSubExpr(visit, ast):
    par = arithExpr(visit, ast)

    left, right = ast.children
    child_types = set(child.root['type'] for child in ast.children)

    if 'addSubExpr' in child_types and child_types & {'subExpr', 'atomExpr'}:
        if is_next_to_calc(left):
            del left.root['_calc']
            ast.root['_calc'] = 'next'
        elif '_calc' in right.root:
            del right.root['_calc']
            ast.root['_calc'] = 'next'
    return par


@atw_prior.register
def divProdExpr(visit, ast):
    par = arithExpr(visit, ast)

    left, right = ast.children
    child_types = set(child.root['type'] for child in ast.children)

    if 'divProdExpr' in child_types and child_types & {'subExpr', 'atomExpr'}:
        if is_next_to_calc(left):
            del left.root['_calc']
            ast.root['_calc'] = 'next'
        elif '_calc' in right.root:
            del right.root['_calc']
            ast.root['_calc'] = 'next'
    return par


@atw_prior.register
def powExpr(visit, ast):
    return arithExpr(visit, ast)


@atw_prior.register
def unaryExpr(visit, ast):
    if is_calculable(ast):
        ast.root['_calc'] = 'next'
        return None
    par = visit(ast.children[0])
    if is_next_to_calc(par):
        return ast
    return par


@atw_prior.register
def fractExpr(visit, ast):
    return arithExpr(visit, ast)


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
