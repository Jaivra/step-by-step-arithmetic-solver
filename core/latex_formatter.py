from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree, Stack

from core.block_depth import BlockDepth
from core.util import *

atw_latex_formatter = AnnotatedTreeWalker('type')

MEMORY = {}
def exec(ast, memory):
    global MEMORY
    MEMORY = memory
    return atw_latex_formatter(ast)



@atw_latex_formatter.register
def atomExpr(visit, ast):
    fr = Fraction(ast.root['value'])
    res = str(fr)
    if fr.denominator != 1:
        res = f'\\frac{{{fr.numerator}}} {{{fr.denominator}}}'
    if '_calc' in ast.root and ast.root['_calc'] == 'last':
        res = f'\\color{{green}}{{\\boxed{{{res}}}}}'
    return res, False


@atw_latex_formatter.register
def addSubExpr(visit, ast):
    op = ast.root['op']

    left, right = ast.children
    left, left_calculable = visit(left)
    right, right_calculable = visit(right)

    if '_calc' in ast.root and ast.root['_calc'] == 'next':
        return f'\\color{{red}}{{\\boxed{{{left}{op}{right}}}}}', True
    return f'{left} {op} {right}', left_calculable or right_calculable


@atw_latex_formatter.register
def divProdExpr(visit, ast):
    op = ast.root['op']

    left, right = ast.children

    left, left_calculable = visit(left)
    right, right_calculable = visit(right)

    if op == 'x':
        op = '\\times'

    if '_calc' in ast.root and ast.root['_calc'] == 'next':
        return f'\\color{{red}}{{\\boxed{{{left}{op}{right}}}}}', True
    return f'{left} {op} {right}', left_calculable or right_calculable


@atw_latex_formatter.register
def powExpr(visit, ast):
    left, right = ast.children

    left, left_calculable = visit(left)
    right, right_calculable = visit(right)

    if '_calc' in ast.root and ast.root['_calc'] == 'next':
        return f'\\color{{red}}{{\\boxed{{{{{left}}}^{{{right}}}}}}}', True
    return f'{{{left}}}^{{{right}}}', left_calculable or right_calculable


@atw_latex_formatter.register
def unaryExpr(visit, ast):
    child, child_calculable = visit(ast.children[0])

    if '_calc' in ast.root and ast.root['_calc'] == 'next':
        return f'\\color{{red}}{{\\boxed{{-{child}}}}}', True
    return f'-{child}', child_calculable


@atw_latex_formatter.register
def fractExpr(visit, ast):
    left, right = ast.children

    left, left_calculable = visit(left)
    right, right_calculable = visit(right)

    if '_calc' in ast.root and ast.root['_calc'] == 'next':
        return f'\\color{{red}}{{\\boxed{{\\frac{{{left}}} {{{right}}}}}}}', True
    return f'\\frac{{{left}}} {{{right}}}', left_calculable or right_calculable


@atw_latex_formatter.register
def roundBlockExpr(visit, ast):
    child, calc = visit(ast.children[0])
    if calc:
        return f'\\color{{blue}}{{\\left({child}\\right)}}', False
    return f'\\left({child}\\right)', False


@atw_latex_formatter.register
def squareBlockExpr(visit, ast):
    child, calc = visit(ast.children[0])
    if calc:
        return f'\\color{{blue}}{{\\left[{child}\\right]}}', False
    return f'\\left[{child}\\right]', False


@atw_latex_formatter.register
def curlyBlockExpr(visit, ast):
    child, calc = visit(ast.children[0])
    if calc:
        return f'\\color{{blue}}{{\\left\\{{{child}\\right\\}}}}', False
    return f'\\left\\{{{child}\\right\\}}', False


@atw_latex_formatter.register
def subExpr(visit, ast):
    return visit(MEMORY[ast.root['ID']])


@atw_latex_formatter.register
def main(visit, ast):
    return visit(ast.children[0])