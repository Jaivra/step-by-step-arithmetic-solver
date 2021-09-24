from collections import namedtuple
import re

from liblet import Stack, Tree

from core.MalformedExpression import MalformedExpression
from core.config import *
from core.util import *


class ShuntingYardParser:
    class TokenStack(Stack):
        def __init__(self, *kwargs):
            super().__init__(*kwargs)
            self.cnt = 0

        def pop(self):
            self.cnt += 1
            return super().pop()

        @property
        def last_count(self):
            return self.cnt - 1

    class OperatorInfo:
        def __init__(self, prec, assoc, operator_type):
            self._prec = prec
            self._assoc = assoc
            self._operator_type = operator_type

        @property
        def operator_type(self):
            return self._operator_type

        def __gt__(self, other):
            if self._operator_type == 'B' and other._operator_type == 'B':
                return self._prec > other._prec or (self._prec == other._prec and self._assoc == 'L')
            if self._operator_type == 'U' and other._operator_type == 'B':
                return self._prec >= other._prec
            if other._operator_type == 'U' or self._operator_type == 'S':
                return False
            return False

    operators = {
        "+": OperatorInfo(0, "L", "B"),
        "-": OperatorInfo(0, "L", "B"),
        ":": OperatorInfo(1, "L", "B"),
        "x": OperatorInfo(1, "L", "B"),
        "/": OperatorInfo(2, "L", "B"),
        "++": OperatorInfo(3, "R", "U"),  # unconsidered
        "--": OperatorInfo(3, "R", "U"),
        "^": OperatorInfo(4, "R", "B"),
        "#": OperatorInfo(-1, '', 'S')
    }
    SENTINEL = '#'

    @property
    def unary_operators(self):
        return {k for k, v in self.operators.items() if v.operator_type == 'U'}

    @property
    def binary_operators(self):
        return {k for k, v in self.operators.items() if v.operator_type == 'B'}

    def __init__(self):
        self.operator_st = Stack()
        self.operand_st = Stack()

    @staticmethod
    def generate_un_op_node(op, subexpr):
        if op == '++':
            return subexpr
        # nel caso del meno unario ci serve una sola sottoespressione
        elif op == '--':
            priority = max(PRIORITY['unaryExpr'], subexpr.root['priority'])
            return Tree({'type': 'unaryExpr', 'op': op[0], 'priority': priority}, [subexpr])
        else:
            raise Exception(f'{op} non è un operatore unario')

    @staticmethod
    def generate_bin_op_node(op, left, right):
        if op == '+' or op == '-':
            priority = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])
            return Tree({'type': 'addSubExpr', 'op': op, 'priority': priority}, [left, right])

        elif op == 'x' or op == ':':
            priority = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])
            return Tree({'type': 'divProdExpr', 'op': op, 'priority': priority}, [left, right])

        elif op == '/':
            priority = max(PRIORITY['fractExpr'], left.root['priority'], right.root['priority'])
            return Tree({'type': 'fractExpr', 'priority': priority}, [left, right])

        elif op == '^':
            priority = max(PRIORITY['powExpr'], left.root['priority'], right.root['priority'])
            return Tree({'type': 'powExpr', 'priority': priority}, [left, right])
        else:
            raise MalformedExpression(
                '{op} non è un operatore binario',
                '',
                [],
                []
            )

    def pop_operator(self):
        if self.operator_st.peek() not in self.operators.keys():
            raise Exception(f'{self.operator_st.peek()} non è un operatore aritmetico')
        if self.operators[self.operator_st.peek()].operator_type == 'B':  # controlla il tipo di operatore
            right, left = self.operand_st.pop(), self.operand_st.pop()
            node = self.generate_bin_op_node(self.operator_st.pop(), left, right)
        else:
            node = self.generate_un_op_node(self.operator_st.pop(), self.operand_st.pop())
        self.operand_st.push(node)

    def push_operator(self, op):

        while self.operators[self.operator_st.peek()] > self.operators[op]:
            self.pop_operator()
        self.operator_st.push(op)

    def parse(self, expr):
        all_tokens = tokenize(expr)
        tokens = []
        unary = True

        for token in all_tokens:
            if unary and token in {'+', '-'}:
                tokens.append(token * 2)
            else:
                tokens.append(token)
            if re.match(r'[\+\*\-\/\^:|x|\(|\{|\<]+$', token):
                unary = True
            else:
                unary = False

        tokens_st = ShuntingYardParser.TokenStack(reversed(tokens))

        def P():
            token = tokens_st.pop()

            if is_integer(token):  # integer atom
                atom = Tree({'type': 'atomExpr', 'value': int(token), 'priority': 0})
                self.operand_st.push(atom)

            elif is_float(token):
                atom = Tree({'type': 'atomExpr', 'value': float(token), 'priority': 0})
                self.operand_st.push(atom)

            elif token in {'(', '<', '[', '{'}:
                self.operator_st.push(self.SENTINEL)
                open_par_pos = tokens_st.last_count
                E()

                close_par = tokens_st.pop() if tokens_st else None

                if token == '(' and close_par == ')':
                    self.operand_st.push(Tree({'type': 'roundBlockExpr', 'priority': 0}, [self.operand_st.pop()]))
                elif token == '[' and close_par == ']':
                    self.operand_st.push(Tree({'type': 'squareBlockExpr', 'priority': 0}, [self.operand_st.pop()]))
                elif token == '{' and close_par == '}':
                    self.operand_st.push(Tree({'type': 'curlyBlockExpr', 'priority': 0}, [self.operand_st.pop()]))
                elif token == '<' and close_par == '>':
                    ...
                else:
                    print(tokens_st.last_count)
                    raise MalformedExpression(
                        f"La parentesi in posizione {open_par_pos} non è stata chiusa!",
                        tokens,
                        [open_par_pos],
                        [])
                self.operator_st.pop()


            elif token in self.unary_operators:
                self.push_operator(token)
                P()
            else:
                raise MalformedExpression(
                    f'Token "{token}" in posizione "{tokens_st.last_count}" non valido',
                    tokens,
                    [tokens_st.last_count],
                    []
                )

        def E():
            P()
            while tokens_st and tokens_st.peek() in self.binary_operators:
                token = tokens_st.pop()

                self.push_operator(token)
                P()
            while self.operator_st.peek() != self.SENTINEL:
                self.pop_operator()

        self.operator_st.push(self.SENTINEL)
        E()
        if tokens_st:
            raise MalformedExpression(
                f'Token  "{tokens_st.pop()}" in posizione "{tokens_st.last_count}" non valido',
                tokens,
                [tokens_st.last_count],
                []
            )
        res = self.operand_st.pop()
        if is_container(res):
            res = res.children[0]
        return Tree({'type': 'main'}, [res])
