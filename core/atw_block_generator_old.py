from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree, Stack

from core.block_depth import *
from core.my_atw import MyAtw
from core.util import *


class AtwBlockGeneratorOld(MyAtw):

    def __init__(self):
        super().__init__('type')
        self._stack = Stack()

    def start(self, ast):
        _, blocks = self(ast)
        return sorted(blocks, key=lambda x: x[0], reverse=True)

    def catchall(self, ast):
        blocks = []
        children = []
        for child in ast.children:
            t, b = self(child)
            children.append(t)
            blocks = blocks + b
        return Tree(ast.root, children), blocks

    def _atw_roundBlockExpr(self, ast):
        return self._blockExpr(ast, BLOCK_TYPE.ROUND)

    def _atw_squareBlockExpr(self, ast):
        return self._blockExpr(ast, BLOCK_TYPE.SQUARE)

    def _atw_curlyBlockExpr(self, ast):
        return self._blockExpr(ast, BLOCK_TYPE.CURLY)

    def _blockExpr(self, ast, block_type):
        block_depth = self._stack.peek().add_block(block_type)
        self._stack.push(block_depth)
        sub_expr, blocks = self(ast.children[0])
        self._stack.pop()
        res = Tree(ast.root, [sub_expr])
        return Tree({'type': 'subExpr', 'ID': block_depth, 'priority': 0}, []), [(block_depth, res)] + blocks

    def _atw_main(self, ast):
        block_depth = BlockDepth()
        self._stack.push(block_depth)
        sub_expr, blocks = self(ast.children[0])
        self._stack.pop()
        res = Tree({'type': 'main'}, [sub_expr])

        return Tree({'type': 'subExpr', 'ID': block_depth, 'priority': 0}, []), [(block_depth, res)] + blocks