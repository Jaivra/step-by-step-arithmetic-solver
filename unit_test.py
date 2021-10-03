import unittest

from core.arithmetic_manager import ArithManager
from core.expression_generator import generate_expression
from core.my_exception import *
from core.util import *
import math


class MyTester(unittest.TestCase):

    def test_parser(self):
        AM_N = ArithManager('N')
        ast = AM_N.shuntingYardExpr2ast("(2 + 3 x 5) / 3 + 1")

        self.assertEqual(ast.__repr__().replace(' ', ''),
                         "({'type': 'main'}: ({'type': 'addSubExpr', 'op': '+', 'priority': 3}: ({'type': 'fractExpr', 'priority': 3}: ({'type': 'roundBlockExpr', 'priority': 0}: ({'type': 'addSubExpr', 'op': '+', 'priority': 2}: ({'type': 'atomExpr', 'value': 2, 'priority': 0}), ({'type': 'divProdExpr', 'op': 'x', 'priority': 2}: ({'type': 'atomExpr', 'value': 3, 'priority': 0}), ({'type': 'atomExpr', 'value': 5, 'priority': 0})))), ({'type': 'atomExpr', 'value': 3, 'priority': 0})), ({'type': 'atomExpr', 'value': 1, 'priority': 0})))".replace(
                             ' ', ''))
        self.assertRaises(DomainError, lambda: AM_N.shuntingYardExpr2ast("(-2 + 3 x 5) / 3 + 1"))
        self.assertRaises(MalformedExpression, lambda: AM_N.shuntingYardExpr2ast("(-2 + 3 x 5 / 3 + 1"))

        AM_R = ArithManager('Q')
        ast = AM_R.shuntingYardExpr2ast("-2^-2/3")
        self.assertEqual(ast.__repr__().replace(' ', ''),
                         "({'type': 'main'}: ({'type': 'fractExpr', 'priority': 5}: ({'type': 'unaryExpr', 'op': '-', 'priority': 5}: ({'type': 'powExpr', 'priority': 5}: ({'type': 'atomExpr', 'value': 2, 'priority': 0}), ({'type': 'atomExpr', 'value': -2, 'priority': 0}))), ({'type': 'atomExpr', 'value': 3, 'priority': 0})))".replace(
                             ' ', ''))

    def test_blocks(self):
        AM_R = ArithManager('R')
        ast = Tree({'type': 'main'}, [
            Tree({'type': 'fractExpr', 'priority': 3}, [
                Tree({'type': 'roundBlockExpr', 'priority': 0}, [
                    Tree({'type': 'divProdExpr', 'op': 'x', 'priority': 2}, [
                        Tree({'type': 'atomExpr', 'value': 2.3, 'priority': 0}),
                        Tree({'type': 'atomExpr', 'value': 5, 'priority': 0}, [])
                    ])
                ]),
                Tree({'type': 'roundBlockExpr', 'priority': 0}, [
                    Tree({'type': 'addSubExpr', 'op': '+', 'priority': 1}, [
                        Tree({'type': 'atomExpr', 'value': 3, 'priority': 0}, []),
                        Tree({'type': 'atomExpr', 'value': 1, 'priority': 0}, [])
                    ])
                ])
            ]),
        ])  # (2.3 x 5) / (3 + 1)

        blocks = AM_R.blocks(ast)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0].__repr__().replace(' ', ''),
                         "('0', ({'type': 'roundBlockExpr', 'priority': 0}: ({'type': 'divProdExpr', 'op': 'x', 'priority': 2}: ({'type': 'atomExpr', 'value': 2.3, 'priority': 0}), ({'type': 'atomExpr', 'value': 5, 'priority': 0}))))".replace(
                             ' ', ''))
        self.assertEqual(blocks[1].__repr__().replace(' ', ''),
                         "('1', ({'type': 'roundBlockExpr', 'priority': 0}: ({'type': 'addSubExpr', 'op': '+', 'priority': 1}: ({'type': 'atomExpr', 'value': 3, 'priority': 0}), ({'type': 'atomExpr', 'value': 1, 'priority': 0}))))".replace(
                             ' ', ''))
        self.assertEqual(blocks[2].__repr__().replace(' ', ''),
                         "('2', ({'type': 'main'}: ({'type': 'fractExpr', 'priority': 3}: ({'type': 'subExpr', 'ID': '0', 'priority': 0}), ({'type': 'subExpr', 'ID': '1', 'priority': 0}))))".replace(
                             ' ', ''))

    def test_prior(self):
        AM_Q = ArithManager('Q')
        ast = Tree({'type': 'main'}, [
            Tree({'type': 'addSubExpr', 'op': '+', 'priority': 5}, [
                Tree({'type': 'atomExpr', 'value': Fraction(2, 3), 'priority': 0}, []),
                Tree({'type': 'divProdExpr', 'op': 'x', 'priority': 5}, [
                    Tree({'type': 'powExpr', 'priority': 5}, [
                        Tree({'type': 'atomExpr', 'value': 5, 'priority': 0}, []),
                        Tree({'type': 'atomExpr', 'value': 3, 'priority': 0}, [])
                    ]),
                    Tree({'type': 'atomExpr', 'value': 3, 'priority': 0}, [])
                ]),
            ]),
        ])  # 2/3 + 5^3 x 3
        parent_to_calc = AM_Q.prior(ast)
        self.assertEqual(parent_to_calc.__repr__().replace(' ', ''),
                         "({'type': 'divProdExpr', 'op': 'x', 'priority': 2}: ({'type': 'powExpr', 'priority': 0, '_calc': 'next'}: ({'type': 'atomExpr', 'value': 5, 'priority': 0}), ({'type': 'atomExpr', 'value': 3, 'priority': 0})), ({'type': 'atomExpr', 'value': 3, 'priority': 0}))".replace(
                             ' ', ''))
        self.assertEqual(ast.__repr__().replace(' ', ''),
                         "({'type': 'main'}: ({'type': 'addSubExpr', 'op': '+', 'priority': 2}: ({'type': 'atomExpr', 'value': Fraction(2, 3), 'priority': 0}), ({'type': 'divProdExpr', 'op': 'x', 'priority': 2}: ({'type': 'powExpr', 'priority': 0, '_calc': 'next'}: ({'type': 'atomExpr', 'value': 5, 'priority': 0}), ({'type': 'atomExpr', 'value': 3, 'priority': 0})), ({'type': 'atomExpr', 'value': 3, 'priority': 0}))))".replace(
                             ' ', ''))

    def test_eval(self):
        AM_Z = ArithManager('Z')
        ast = Tree({'type': 'main'}, [
            Tree({'type': 'divProdExpr', 'op': 'x', 'priority': 2}, [
                Tree({'type': 'divProdExpr', 'op': 'x', 'priority': 2}, [
                    Tree({'type': 'atomExpr', 'value': 5, 'priority': 0}, []),
                    Tree({'type': 'atomExpr', 'value': -2, 'priority': 0}, [])
                ]),
                Tree({'type': 'atomExpr', 'value': 3, 'priority': 0}, [])
            ]),
        ])  # 5 x -2 x 3
        res = AM_Z.eval(ast)
        self.assertEqual(res, -30)

    def test_latex(self):
        AM_N = ArithManager('Q')
        main_block = Tree({'type': 'main'}, [
            Tree({'type': 'addSubExpr', 'op': '+', 'priority': 1}, [
                Tree({'type': 'subExpr', 'ID': '38', 'priority': 0}, []),
                Tree({'type': 'atomExpr', 'value': 2, 'priority': 0}, [])
            ])
        ])
        MEM = {'38': Tree({'type': 'roundBlockExpr', 'priority': 0}, [
            Tree({'type': 'addSubExpr', 'op': '+', 'priority': 1}, [
                Tree({'type': 'atomExpr', 'value': Fraction(4, 3), 'priority': 0}, []),
                Tree({'type': 'divProdExpr', 'op': 'x', 'priority': 0, '_calc': 'next'}, [
                    Tree({'type': 'atomExpr', 'value': 16, 'priority': 0, '_calc': 'last'}, []),
                    Tree({'type': 'atomExpr', 'value': 3, 'priority': 0}, [])
                ]),
            ])
        ])}

        # (4/3 + 16 x 3) + 2, con appena calcolato il valore 16
        latex = AM_N.latex(main_block, MEM)
        self.assertEqual(latex.replace(' ', ''),
                         r'\color{blue}{\left(\frac{4}{3}+\color{red}{\boxed{\color{green}{\boxed{16}}\times3}}\right)}+2')

        # deve aver tolto l'annotazione _calc : last sul 16
        self.assertEqual(MEM['38'].__repr__().replace(' ', ''),
                         "({'type': 'roundBlockExpr', 'priority': 0}: ({'type': 'addSubExpr', 'op': '+', 'priority': 1}: ({'type': 'atomExpr', 'value': Fraction(4, 3), 'priority': 0}), ({'type': 'divProdExpr', 'op': 'x', 'priority': 0, '_calc': 'next'}: ({'type': 'atomExpr', 'value': 16, 'priority': 0}), ({'type': 'atomExpr', 'value': 3, 'priority': 0}))))".replace(
                             ' ', ''))

    def test_expr_solver(self, count=10):
        def solve(expr, domain):
            AM = ArithManager(domain)
            ast = AM.shuntingYardExpr2ast(expr)
            blocks = AM.blocks(ast)
            MEMORY = dict(blocks)
            main_block = blocks[-1][1]
            while blocks and is_calculable(blocks[0][1]): blocks = blocks[1:]
            while blocks:
                block_id, current_block = blocks[0]
                parent_to_calc = AM.prior(current_block)
                parent_to_calc.children = [
                    Tree({'type': 'atomExpr', 'value': AM.eval(child, MEMORY), 'priority': 0, '_calc': 'last'}, [])
                    if is_next_to_calc(child) else child
                    for child in parent_to_calc.children]
                if is_calculable(current_block):
                    current_block = current_block.children[0]
                    blocks = blocks[1:]
                MEMORY[block_id] = current_block
            return main_block.children[0].root['value']

        for _ in range(count):
            expr = generate_expression(2)
            try:
                # print(expr)
                shunting_res = solve(expr, 'R')
            except Exception as e:
                print('** EXCEPTION SHUNTING ** ', expr, e)
                continue
            formatted_expr = expr.replace('x', '*').replace(':', '/').replace('^', '**')
            res = eval(formatted_expr)
            self.assertEqual(math.isclose(res, shunting_res, rel_tol=1e-9, abs_tol=0.0), True)


if __name__ == '__main__':
    tester = MyTester()
    tester.test_parser()
    tester.test_blocks()
    tester.test_prior()
    tester.test_eval()
    tester.test_latex()
    tester.test_expr_solver(100)
