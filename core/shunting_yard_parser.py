from collections import namedtuple
import re

from liblet import Stack, Tree

from core.config import PRIORITY
from core.util import *


class ShuntingYardParser:
    opinfo = namedtuple('Operator', 'prec assoc type')
    operators = {
        "+": opinfo(0, "L", "bin"),
        "-": opinfo(0, "L", "bin"),
        ":": opinfo(1, "L", "bin"),
        "x": opinfo(1, "L", "bin"),
        "++": opinfo(2, "R", "un"),  # unconsidered
        "--": opinfo(2, "R", "un"),
        "/": opinfo(3, "L", "bin"),
        "^": opinfo(4, "R", "bin"),
    }

    def __init__(self):
        self.operator_st = Stack()
        self.operand_st = Stack()


    def generate_op_node(self):
        def generate_un_op_node(op, subexpr):
            if op == '++': return subexpr

            if op == '--':
                priority = max(PRIORITY['unaryExpr'], subexpr.root['priority'])
                return Tree({'type': 'unaryExpr', 'op': op[0], 'priority': priority}, [subexpr])

        def generate_bin_op_node(op, left, right):
            if op == '+' or op == '-':
                priority = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])
                return Tree({'type': 'addSubExpr', 'op': op, 'priority': priority}, [left, right])

            if op == 'x' or op == ':':
                priority = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])
                return Tree({'type': 'divProdExpr', 'op': op, 'priority': priority}, [left, right])

            if op == '/':
                priority = max(PRIORITY['fractExpr'], left.root['priority'], right.root['priority'])
                return Tree({'type': 'fractExpr', 'priority': priority}, [left, right])

            if op == '^':
                priority = max(PRIORITY['powExpr'], left.root['priority'], right.root['priority'])
                return Tree({'type': 'powExpr', 'priority': priority}, [left, right])

        if self.operators[self.operator_st.peek()].type == 'bin':
            right, left = self.operand_st.pop(), self.operand_st.pop()
            node = generate_bin_op_node(self.operator_st.pop(), left, right)
        else:
            node = generate_un_op_node(self.operator_st.pop(), self.operand_st.pop())
        return node



    def parse(self, expr):
        clean_expr = expr.split()
        tokens = list(clean_expr)
        last_token = None




        while tokens:
            token = tokens[0]

            if token == '+' and last_token in set(self.operators.keys() | {'<', '(', '[', '{', None}): # ignore + unary
                tokens = tokens[1:]
                continue

            if token == '-' and last_token in set(self.operators.keys() | {'<', '(', '[', '{', None}): # - unary
                if tokens[1][0].isdigit(): # if - is part of number
                    tokens[1] = f'-{tokens[1]}'
                    tokens = tokens[1:]
                    continue
                token = token * 2

            if is_integer(token):  # integer atom
                atom = Tree({'type': 'atomExpr', 'value': int(token), 'priority': 0})
                self.operand_st.push(atom)

            elif is_float(token):
                atom = Tree({'type': 'atomExpr', 'value': float(token), 'priority': 0})
                self.operand_st.push(atom)

            elif is_rational(token):  # rational atom
                num, den = token.split('/')
                atom = Tree({'type': 'atomExpr', 'value': Fraction(int(num), int(den)), 'priority': 0})
                self.operand_st.push(atom)

            elif token == '--' and last_token in {'^', '/'}: # caso non coperto dall'algoritmo, quando il meno unario è dopo il fract o pow ha priorità maggiore
                self.operator_st.push(token)

            elif token in self.operators.keys():  # operator
                while self.operator_st and self.operator_st.peek() not in {'(', '<', '[', '{'} and \
                        (self.operators[self.operator_st.peek()].prec > self.operators[token].prec or
                         (self.operators[self.operator_st.peek()].prec == self.operators[token].prec and
                          self.operators[token].assoc == 'L')):
                    self.operand_st.push(self.generate_op_node())
                self.operator_st.push(token)

            elif token in {'(', '<', '[', '{'}:
                self.operator_st.push(token)

            elif token in {')', ']', '}'}:
                if token == ')':
                    open_brack = '('
                    bracket_type = 'roundBlockExpr'
                elif token == ']':
                    open_brack = '['
                    bracket_type = 'squareBlockExpr'
                else:
                    open_brack = '{'
                    bracket_type = 'curlyBlockExpr'

                while self.operator_st.peek() != open_brack:
                    self.operand_st.push(self.generate_op_node())

                if not is_container(self.operand_st.peek()) and not is_atom(self.operand_st.peek()):
                    block = Tree({'type': bracket_type, 'priority': 0}, [self.operand_st.pop()])
                    self.operand_st.push(block)
                self.operator_st.pop()

            elif token == '>':
                while self.operator_st.peek() != '<':
                    self.operand_st.push(self.generate_op_node())
                self.operator_st.pop()

            # print(token, self.operand_st, self.operator_st)

            last_token = token
            tokens = tokens[1:]

        while self.operator_st:
            self.operand_st.push(self.generate_op_node())

        res = self.operand_st.pop()
        if is_container(res):
            res = res.children[0]
        return Tree({'type': 'main'}, [res])
