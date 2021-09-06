from liblet import ANTLR

from core.block_generator import exec as block_generator
from core.ptree_to_ast import exec as ptree_to_ast
from core.expr_eval import exec as expr_eval
from core.latex_formatter import exec as latex_formatter
from core.block_priority import exec as priority


class ArithManager:


    @staticmethod
    def arith_expr(grammar_file):
        with open(grammar_file, 'r') as reader:
            return ANTLR(reader.read())

    @staticmethod
    def ptree(arith, expr):
        return arith.tree(expr, 's')

    @staticmethod
    def ptree2ast(ptree):
        return ptree_to_ast(ptree)

    @staticmethod
    def generate_blocks(ast):
        _, blocks = block_generator(ast)
        return sorted(blocks, key=lambda x: x[0], reverse=True)

    @staticmethod
    def annotate_with_priority(ast):
        return priority(ast)

    @staticmethod
    def eval(ast, memory=None):
        if memory is None:
            memory = dict()
        return expr_eval(ast, memory)

    @staticmethod
    def latex_format(ast, memory):
        return latex_formatter(ast, memory)
