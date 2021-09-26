from liblet import Stack

from core.expr_block import ExprBlock, BLOCK_TYPE
from core.my_atw import MyAtw
from core.util import *


class AtwBlockGenerator(MyAtw):

    def __init__(self):
        super().__init__('type')
        self._stack = Stack()

    def start(self, ast):
        _, block = self(ast)
        block = block[0]
        trees = block.generate_sorted_trees_list()
        return trees

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
        sub_expr, blocks = self(ast.children[0])

        res = Tree(ast.root, [sub_expr])
        block = ExprBlock(block_type, blocks, res)
        return Tree({'type': 'subExpr', 'ID': block.ID, 'priority': 0}, []), [block]

    def _atw_main(self, ast):
        sub_expr, blocks = self(ast.children[0])
        res = Tree({'type': 'main'}, [sub_expr])
        main_block = ExprBlock(BLOCK_TYPE.INIT, blocks, res)
        main_block.build()
        return Tree({'type': 'subExpr', 'ID': main_block.ID, 'priority': 0}, []), [main_block]
