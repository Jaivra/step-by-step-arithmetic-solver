from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree

from core.config import PRIORITY
from core.my_atw import MyAtw
from core.util import *


class AtwPtreeToAst(MyAtw):

    def __init__(self):
        super().__init__('name')

    def start(self, ptree):
        return self(ptree)

    def _atw_RAT(self, ptree):
        return Fraction(ptree.root['value'])

    def _atw_INT(self, ptree):
        return int(ptree.root['value'])

    def _atw_REAL(self, ptree):
        return float(ptree.root['value'])

    def _atw_atomExpr(self, ptree):
        if len(ptree.children) > 1:
            value = -self(ptree.children[1])
        else:
            value = self(ptree.children[0])
        return Tree({'type': 'atomExpr', 'value': value, 'priority': 0}, [])

    def _atw_addSubExpr(self, ptree):
        left, op, right = ptree.children
        left = self(left)
        right = self(right)

        priority = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'addSubExpr', 'op': op.root['value'], 'priority': priority}, [left, right])

    def _atw_divProdExpr(self, ptree):
        left, op, right = ptree.children
        left = self(left)
        right = self(right)

        priority = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'divProdExpr', 'op': op.root['value'], 'priority': priority}, [left, right])

    def _atw_powExpr(self, ptree):
        left, _, right = ptree.children
        left = self(left)
        right = self(right)

        priority = max(PRIORITY['powExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'powExpr', 'priority': priority}, [left, right])

    def _atw_unaryExpr(self, ptree):
        op, subexpr = ptree.children
        subexpr = self(subexpr)
        if op.root['value'] == '+':
            return subexpr
        if is_atom(subexpr):
            return Tree({'type': 'atomExpr', 'value': -subexpr.root['value'], 'priority': 0}, [])

        priority = max(PRIORITY['unaryExpr'], subexpr.root['priority'])
        return Tree({'type': 'unaryExpr', 'op': op.root['value'], 'priority': priority}, [subexpr])

    def _atw_fractExpr(self, ptree):
        left, _, right = ptree.children
        left = self(left)
        right = self(right)

        priority = max(PRIORITY['fractExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'fractExpr', 'priority': priority}, [left, right])

    def _atw_roundBlockExpr(self, ptree):
        _, subexpr, _ = ptree.children
        subexpr = self(subexpr)

        if is_container(subexpr) or is_atom(subexpr):
            return subexpr
        return Tree({'type': 'roundBlockExpr', 'priority': 0}, [subexpr])

    def _atw_squareBlockExpr(self, ptree):
        _, subexpr, _ = ptree.children
        subexpr = self(subexpr)

        if is_container(subexpr) or is_atom(subexpr):
            return subexpr
        return Tree({'type': 'squareBlockExpr', 'priority': 0}, [subexpr])

    def _atw_curlyBlockExpr(self, ptree):
        _, subexpr, _ = ptree.children
        subexpr = self(subexpr)

        if is_container(subexpr) or is_atom(subexpr):
            return subexpr
        return Tree({'type': 'curlyBlockExpr', 'priority': 0}, [subexpr])

    def _atw_subExpr(self, ptree):
        _, subexpr, _ = ptree.children
        return self(subexpr)

    def _atw_s(self, ptree):
        expr = self(ptree.children[0])
        if is_container(expr):
            expr = expr.children[0]
        return Tree({'type': 'main'}, [expr])
