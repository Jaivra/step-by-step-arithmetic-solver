from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree, Stack

from core.block_depth import BlockDepth
from core.config import PRIORITY
from core.my_atw import MyAtw
from core.util import *

atw_prior = AnnotatedTreeWalker('type')


class AtwBlockPriority(MyAtw):
    def __init__(self):
        super().__init__('type')

    def start(self, ast):
        return self(ast)

    def _atw_atomExpr(self, ast):
        return None

    def _atw_subExpr(self, ast):
        return None

    def _arithExpr(self, ast):
        if is_calculable(ast):
            ast.root['_calc'] = 'next'
            ast.root['priority'] = 0
            return None

        left, right = ast.children
        if left.root['priority'] >= right.root['priority']:
            par = self(left)
        else:
            par = self(right)

        if is_next_to_calc(left) or is_next_to_calc(right):
            return ast
        return par

    def _atw_addSubExpr(self, ast):
        par = self._arithExpr(ast)

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

    def _atw_divProdExpr(self, ast):
        par = self._arithExpr(ast)

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

    def _atw_powExpr(self, ast):
        par = self._arithExpr(ast)
        if not is_next_to_calc(ast):
            ast.root['priority'] = max(PRIORITY['powExpr'], ast.children[0].root['priority'])
        return par

    def _atw_unaryExpr(self, ast):
        if is_calculable(ast):
            ast.root['_calc'] = 'next'
            return None
        par = self(ast.children[0])
        ast.root['priority'] = max(PRIORITY['unaryExpr'], ast.children[0].root['priority'])

        if is_next_to_calc(ast.children[0]):
            return ast
        return par

    def _atw_fractExpr(self, ast):
        par = self._arithExpr(ast)
        if not is_next_to_calc(ast):
            ast.root['priority'] = max(PRIORITY['fractExpr'], ast.children[0].root['priority'])
        return par

    def _container(self, ast):
        par = self(ast.children[0])
        if is_next_to_calc(ast.children[0]):
            return ast
        return par

    def _atw_main(self, ast):
        return self._container(ast)

    def _atw_roundBlockExpr(self, ast):
        return self._container(ast)

    def _atw_squareBlockExpr(self, ast):
        return self._container(ast)

    def _atw_curlyBlockExpr(self, ast):
        return self._container(ast)
