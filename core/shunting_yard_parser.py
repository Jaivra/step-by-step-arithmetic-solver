from collections import namedtuple
import re

from liblet import Stack, Tree

from core.config import PRIORITY
from core.util import *


class ShuntingYardParser:
    opinfo = namedtuple('Operator', 'prec assoc')
    operators = {
        "+": opinfo(0, "L"),
        "-": opinfo(0, "L"),
        ":": opinfo(1, "L"),
        "x": opinfo(1, "L"),
        "/": opinfo(2, "L"),
        "^": opinfo(3, "R"),
    }

    def __init__(self):
        self.operator_st = Stack()
        self.operand_st = Stack()

    def _generate_op_node(self, op, left, right):

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

    def parse(self, expr):
        clean_expr = expr.split()
        tokens = list(clean_expr)
        while tokens:
            token = tokens[0]
            if token.isdigit():
                atom = Tree({'type': 'atomExpr', 'value': int(token), 'priority': 0})
                self.operand_st.push(atom)
            elif re.match('[0-9]+/[0-9]+$', token):
                num, den = token.split('/')
                atom = Tree({'type': 'atomExpr', 'value': Fraction(int(num), int(den)), 'priority': 0})
                self.operand_st.push(atom)

            elif token in self.operators.keys():
                while self.operator_st and self.operator_st.peek() not in {'(', '<', '[', '{'} and \
                        (self.operators[self.operator_st.peek()].prec > self.operators[token].prec or
                         (self.operators[self.operator_st.peek()].prec == self.operators[token].prec and self.operators[
                             token].assoc == 'L')):
                    # print("****", q)
                    right = self.operand_st.pop()
                    left = self.operand_st.pop()
                    node = self._generate_op_node(self.operator_st.pop(), left, right)
                    self.operand_st.push(node)
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
                    right = self.operand_st.pop()
                    left = self.operand_st.pop()
                    node = self._generate_op_node(self.operator_st.pop(), left, right)
                    self.operand_st.push(node)
                if not is_container(self.operand_st.peek()) and not is_atom(self.operand_st.peek()):
                    block = Tree({'type': bracket_type, 'priority': 0}, [self.operand_st.pop()])
                    self.operand_st.push(block)
                self.operator_st.pop()

            elif token == '>':
                while self.operator_st.peek() != '<':
                    right = self.operand_st.pop()
                    left = self.operand_st.pop()
                    node = self._generate_op_node(self.operator_st.pop(), left, right)
                    self.operand_st.push(node)
                self.operator_st.pop()
            tokens = tokens[1:]
        while self.operator_st:
            right = self.operand_st.pop()
            left = self.operand_st.pop()
            node = self._generate_op_node(self.operator_st.pop(), left, right)
            self.operand_st.push(node)

        res = self.operand_st.pop()
        if is_container(res):
            res = res.children[0]
        return Tree({'type': 'main'}, [res])
