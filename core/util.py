from IPython.core.display import display, Latex
from liblet import Tree


def is_container(ast):
    return ast.root['type'] in {'roundBlockExpr', 'squareBlockExpr', 'curlyBlockExpr'}

def is_atom(ast):
    return ast.root['type'] == 'atomExpr'

def display_latex(tex):
    display(Latex(fr"""\begin{{align}}{tex}\end{{align}}"""))

def is_calculable(ast):
    return all(child.root['type'] in {'atomExpr', 'subExpr'} for child in ast.children)

def is_next_to_calc(ast):
    return '_calc' in ast.root and ast.root['_calc'] == 'next'

def block2ast(main_block, memory):
    if main_block.root['type'] == 'subExpr':
        return block2ast(memory[main_block.root['ID']], memory)
    return Tree(main_block.root, [block2ast(child, memory) for child in main_block.children])