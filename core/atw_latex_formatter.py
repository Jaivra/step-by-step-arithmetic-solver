from core.my_atw import MyAtw
from fractions import Fraction

"""
Walker che riceve in input un AST di un espressione e un dizionario contenente i vari risultati delle sottoespressioni. 
Ha il compito di restituire la stringa latex formattata corrispondente all'espressione.
Sarà utilizzato sempre passando il blocco contenente l'espressione completa.
"""
class AtwLatexFormatter(MyAtw):

    def __init__(self):
        super().__init__('type')
        self._MEMORY = {}

    def start(self, ast, MEMORY):
        self._MEMORY = MEMORY
        tex, _ = self(ast)
        return tex

    def _atw_atomExpr(self, ast):
        res = str(ast.root['value'])

        if isinstance(ast.root['value'], Fraction):
            fr = Fraction(ast.root['value'])
            res = f'\\frac{{{fr.numerator}}}{{{fr.denominator}}}'
        if isinstance(ast.root['value'], float):
            res = str(round(ast.root['value'], 3))
        if '_calc' in ast.root and ast.root['_calc'] == 'last':
            del ast.root['_calc']
            res = f'\\color{{green}}{{\\boxed{{{res}}}}}'
        return res, False

    def _atw_addSubExpr(self, ast):
        op = ast.root['op']

        left, right = ast.children
        left, left_calculable = self(left)
        right, right_calculable = self(right)

        if '_calc' in ast.root and ast.root['_calc'] == 'next':
            return f'\\color{{red}}{{\\boxed{{{left}{op}{right}}}}}', True
        return f'{left}{op}{right}', left_calculable or right_calculable

    def _atw_divProdExpr(self, ast):
        op = ast.root['op']

        left, right = ast.children

        left, left_calculable = self(left)
        right, right_calculable = self(right)

        if op == 'x':
            op = '\\times'

        if '_calc' in ast.root and ast.root['_calc'] == 'next':
            return f'\\color{{red}}{{\\boxed{{{left}{op}{right}}}}}', True
        return f'{left}{op}{right}', left_calculable or right_calculable

    def _atw_powExpr(self, ast):
        left, right = ast.children

        left, left_calculable = self(left)
        right, right_calculable = self(right)

        if '_calc' in ast.root and ast.root['_calc'] == 'next':
            return f'\\color{{red}}{{\\boxed{{{{{left}}}^{{{right}}}}}}}', True
        return f'{{{left}}}^{{{right}}}', left_calculable or right_calculable

    def _atw_unaryExpr(self, ast):
        child, child_calculable = self(ast.children[0])

        if '_calc' in ast.root and ast.root['_calc'] == 'next':
            return f'\\color{{red}}{{\\boxed{{-{child}}}}}', True
        return f'-{child}', child_calculable

    def _atw_fractExpr(self, ast):
        left, right = ast.children

        left, left_calculable = self(left)
        right, right_calculable = self(right)

        if '_calc' in ast.root and ast.root['_calc'] == 'next':
            return f'\\color{{red}}{{\\boxed{{\\frac{{{left}}}{{{right}}}}}}}', True
        return f'\\frac{{{left}}}{{{right}}}', left_calculable or right_calculable

    def _atw_roundBlockExpr(self, ast):
        child, calc = self(ast.children[0])
        if calc:
            return f'\\color{{blue}}{{\\left({child}\\right)}}', False
        return f'\\left({child}\\right)', False

    def _atw_squareBlockExpr(self, ast):
        child, calc = self(ast.children[0])
        if calc:
            return f'\\color{{blue}}{{\\left[{child}\\right]}}', False
        return f'\\left[{child}\\right]', False

    def _atw_curlyBlockExpr(self, ast):
        child, calc = self(ast.children[0])
        if calc:
            return f'\\color{{blue}}{{\\left\\{{{child}\\right\\}}}}', False
        return f'\\left\\{{{child}\\right\\}}', False

    # Recupera la sottoespressione dalla memoria
    def _atw_subExpr(self, ast):
        return self(self._MEMORY[ast.root['ID']])

    def _atw_main(self, ast):
        return self(ast.children[0])