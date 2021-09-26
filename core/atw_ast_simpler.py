from core.config import PRIORITY
from core.my_atw import MyAtw
from core.util import *


class AtwAstSimpler(MyAtw):

    def __init__(self):
        super().__init__('type')

    def start(self, ptree):
        return self(ptree)

    @staticmethod
    def _generate_tree_with_priority(tree, children):
        priority = max([PRIORITY[tree.root['type']]] + [child.root['priority'] for child in children])
        root = tree.root
        root['priority'] = priority
        return Tree(root, children)

    def catchall(self, tree):
        trees = []
        for child in tree.children:
            t = self(child)
            if t is not None: trees.append(t)
        return AtwAstSimpler._generate_tree_with_priority(tree, trees)

    def _atw_unaryExpr(self, ast):
        subexpr = self(ast.children[0])
        if ast.root['op'] == '+':
            return subexpr
        if is_atom(subexpr):
            return Tree({'type': 'atomExpr', 'value': -subexpr.root['value'], 'priority': 0}, [])
        return AtwAstSimpler._generate_tree_with_priority(ast, [subexpr])

    def _atw_fractExpr(self, ast):
        left, right = ast.children
        left = self(left)
        right = self(right)
        if is_atom(left) and is_atom(right):
            return Tree({'type': 'atomExpr', 'value': Fraction(left.root['value'], right.root['value']), 'priority': 0}, [])
        else:
            return AtwAstSimpler._generate_tree_with_priority(ast, [left, right])

    def _atw_roundBlockExpr(self, ast):
        subexpr = self(ast.children[0])

        if is_container(subexpr) or is_atom(subexpr):
            return subexpr
        return Tree(ast.root, [subexpr])

    def _atw_squareBlockExpr(self, ast):
        subexpr = self(ast.children[0])
        if is_container(subexpr) or is_atom(subexpr):
            return subexpr
        return Tree(ast.root, [subexpr])

    def _atw_curlyBlockExpr(self, ast):
        subexpr = self(ast.children[0])
        if is_container(subexpr) or is_atom(subexpr):
            return subexpr
        return Tree(ast.root, [subexpr])


    def _atw_main(self, ptree):
        expr = self(ptree.children[0])
        if is_container(expr):
            expr = expr.children[0]
        return Tree({'type': 'main'}, [expr])
