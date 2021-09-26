from ignore.my_atw import MyAtw
from core.util import *

from operator import add, mul, sub


class AtwEvalExpr(MyAtw):
    ARITH_OP = {
        '+': add,
        '-': sub,
        'x': mul,
        ':': Fraction
    }

    def __init__(self):
        super().__init__('type')
        self.MEMORY = {}

    def start(self, ast, memory):
        self.MEMORY = memory
        return self(ast)

    def _atw_atomExpr(self, ast):
        return ast.root['value']

    def _atw_subExpr(self, ast):
        return self.MEMORY[ast.root['ID']].root['value']

    @check_type
    def _atw_addSubExpr(self, ast):
        left, right = ast.children
        op = ast.root['op']
        left, right = self(left), self(right)
        return AtwEvalExpr.ARITH_OP[op](left, right)

    @check_type
    def _atw_divProdExpr(self, ast):

        left, right = ast.children
        op = ast.root['op']
        left, right = self(left), self(right)
        if op == ':':
            if right == 0: raise ZeroDivisionError(f'Division by 0 --> {left}:{right}')
            elif isinstance(left, float) or isinstance(right, float): value = left / right
            else: value = Fraction(left, right)
        else:
            value = left * right
        return value

    @check_type
    def _atw_powExpr(self, ast):
        left, right = ast.children
        left, right = self(left), self(right)
        if not isinstance(left, float) and isinstance(right, int):
#            value = int(pow(left, right)) if right > 0 else Fraction(1, pow(left, -right))
            value = pow(left, right) if right > 0 else Fraction(1, pow(left, -right))
        else:
            value = pow(left, right)
        #     value = float(pow(left, right))
        return value

    def _atw_unaryExpr(self, ast):
        value = self(ast.children[0])
        if ast.root['op'] == '-':
            value = -value
        return value

    @check_type
    def _atw_fractExpr(self, ast):
        left, right = ast.children
        left, right = self(left), self(right)
        if isinstance(left, float) or isinstance(right, float):
            return left / right
        return Fraction(left, right)

    def _atw_main(self, ast):
        return self(ast.children[0])
