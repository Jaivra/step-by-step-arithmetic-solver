from fractions import Fraction

from liblet import AnnotatedTreeWalker, Tree, Stack

from core.block_depth import BlockDepth
from core.util import *

atw_blocks = AnnotatedTreeWalker('type', AnnotatedTreeWalker.RECOURSE_CHILDREN)

def exec(ast):
    return atw_blocks(ast)

st = Stack()

@atw_blocks.catchall
def catchall(visit, ast):
    blocks = []
    children = []
    for child in ast.children:
        t, b = visit(child)
        children.append(t)
        blocks = blocks + b
    return Tree(ast.root, children), blocks

    # trees = []
    # for child in tree.children:
    # t = visit(child)
    # if t is not None: trees.append(t)
    # return Tree(tree.root, trees)


@atw_blocks.register
def roundBlockExpr(visit, ast):
    block_depth = st.peek().add_block(BlockDepth.ROUND)
    st.push(block_depth)
    sub_expr, blocks = visit(ast.children[0])
    st.pop()
    res = Tree(ast.root, [sub_expr])
    return Tree({'type': 'subExpr', 'ID': block_depth, 'priority': 0}, []), [(block_depth, res)] + blocks


@atw_blocks.register
def squareBlockExpr(visit, ast):
    block_depth = st.peek().add_block(BlockDepth.SQUARE)
    st.push(block_depth)
    sub_expr, blocks = visit(ast.children[0])
    st.pop()
    res = Tree(ast.root, [sub_expr])
    return Tree({'type': 'subExpr', 'ID': block_depth, 'priority': 0}, []), [(block_depth, res)] + blocks


@atw_blocks.register
def curlyBlockExpr(visit, ast):
    block_depth = st.peek().add_block(BlockDepth.CURLY)
    st.push(block_depth)
    sub_expr, blocks = visit(ast.children[0])
    st.pop()
    res = Tree(ast.root, [sub_expr])
    return Tree({'type': 'subExpr', 'ID': block_depth, 'priority': 0}, []), [(block_depth, res)] + blocks


@atw_blocks.register
def main(visit, ast):
    block_depth = BlockDepth()
    st.push(block_depth)
    sub_expr, blocks = visit(ast.children[0])
    st.pop()
    res = Tree({'type': 'main'}, [sub_expr])

    return Tree({'type': 'subExpr', 'ID': block_depth, 'priority': 0}, []), [(block_depth, res)] + blocks