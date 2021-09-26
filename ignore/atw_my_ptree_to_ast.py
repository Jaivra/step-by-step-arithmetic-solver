from core.config import PRIORITY
from ignore.my_atw import MyAtw
from core.util import *


class AtwPtreeToAst(MyAtw):

    def __init__(self):
        super().__init__('name')

    def start(self, ptree):
        return self(ptree)

    def _atw_Add(self, ptree):
        op = ptree.children[1].children[0].root['name']
        if op == 'ε': return self(ptree.children[0])
        left, right = ptree.children
        left, right = self(left), self(right)
        priority = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'addSubExpr', 'op': op, 'priority': priority}, [left, right])

    def _atw_AddAux(self, ptree):
        if len(ptree.children) == 1: return None
        op = ptree.children[2].children[0].root['name']
        if op == 'ε': return self(ptree.children[1])

        left, right = self(ptree.children[1]), self(ptree.children[2])
        priority = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'addSubExpr', 'op': op, 'priority': priority}, [left, right])

    def _atw_Mul(self, ptree):
        op = ptree.children[1].children[0].root['name']
        if op == 'ε': return self(ptree.children[0])
        left, right = ptree.children
        left, right = self(left), self(right)
        priority = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'divProdExpr', 'op': op, 'priority': priority}, [left, right])

    def _atw_MulAux(self, ptree):
        if len(ptree.children) == 1: return None
        op = ptree.children[2].children[0].root['name']
        if op == 'ε': return self(ptree.children[1])

        left, right = self(ptree.children[1]), self(ptree.children[2])
        priority = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'divProdExpr', 'op': op, 'priority': priority}, [left, right])

    def _atw_Fract(self, ptree):
        op = ptree.children[1].children[0].root['name']
        if op == 'ε': return self(ptree.children[0])
        left, right = ptree.children
        left, right = self(left), self(right)
        priority = max(PRIORITY['fractExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'fractExpr', 'priority': priority}, [left, right])

    def _atw_FractAux(self, ptree):
        if len(ptree.children) == 1: return None
        op = ptree.children[2].children[0].root['name']
        if op == 'ε': return self(ptree.children[1])

        left, right = self(ptree.children[1]), self(ptree.children[2])
        priority = max(PRIORITY['fractExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'fractExpr', 'priority': priority}, [left, right])

    def _atw_Pow(self, ptree):
        op = ptree.children[1].children[0].root['name']
        if op == 'ε': return self(ptree.children[0])
        left, right = ptree.children
        left, right = self(left), self(right)
        priority = max(PRIORITY['powExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'powExpr', 'priority': priority}, [left, right])

    def _atw_PowAux(self, ptree):
        if len(ptree.children) == 1: return None
        op = ptree.children[2].children[0].root['name']
        if op == 'ε': return self(ptree.children[1])

        left, right = self(ptree.children[1]), self(ptree.children[2])
        priority = max(PRIORITY['powExpr'], left.root['priority'], right.root['priority'])

        return Tree({'type': 'powExpr', 'priority': priority}, [left, right])

    def _atw_F(self, ptree):
        if len(ptree.children) == 1: return self(ptree.children[0])
        subexpr = self(ptree.children[1])

        parent = ptree.children[0].root['name']
        if is_container(subexpr) or is_atom(subexpr) or parent == '<':
            return subexpr
        if parent == '(':
            parent_type = 'roundBlockExpr'
        elif parent == '[':
            parent_type = 'squareBlockExpr'
        elif parent == '{':
            parent_type = 'curlyBlockExpr'
        return Tree({'type': parent_type, 'priority': 0}, [subexpr])

    def _atw_S(self, ptree):
        expr = self(ptree.children[0])
        if is_container(expr):
            expr = expr.children[0]
        return Tree({'type': 'main'}, [expr])


    def _atw_Num(self, ptree):
        if len(ptree.children) == 1: return None
        left, right = self(ptree.children[0]), self(ptree.children[1])
        if right is not None:
            value = int(f'{left}{right.root["value"]}')
        else:
            value = left
        return Tree({'type': 'atomExpr', 'value': value, 'priority': 0}, [])

    def _atw_Digit(self, ptree):
        return int(ptree.children[0].root['name'])

    def catchall(self, tree):
        trees = []
        for child in tree.children:
            t = self(child)
            if t is not None: trees.append(t)
        return Tree(tree.root, trees)
