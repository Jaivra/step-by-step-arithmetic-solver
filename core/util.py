from IPython.core.display import display, Latex


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