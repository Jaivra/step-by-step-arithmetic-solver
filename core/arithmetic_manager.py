from liblet import ANTLR

from core.atw_ast_simpler import AtwAstSimpler
from core.atw_block_generator import AtwBlockGenerator
from core.atw_block_generator_old import AtwBlockGeneratorOld
from core.atw_latex_formatter import AtwLatexFormatter
from core.atw_ptree_to_ast import AtwPtreeToAst
from core.atw_expr_eval import AtwEvalExpr
from core.atw_block_priority import AtwBlockPriority
from core.shunting_yard_parser_new import ShuntingYardParser
from core.util import *


class ArithManager:

    def __init__(self):
        self._atw_ptree_to_ast = AtwPtreeToAst()
        self._atw_ast_simpler = AtwAstSimpler()
        self._shunting_yard_parser = ShuntingYardParser()
        self._atw_block_generator = AtwBlockGenerator()
        self._atw_latex_formatter = AtwLatexFormatter()
        self._atw_block_priority = AtwBlockPriority()
        self._atw_eval_expr = AtwEvalExpr()

    def ptree(self, grammar_file, expr):
        with open(grammar_file, 'r') as reader:
            expr = ' '.join(tokenize(expr))
            arith = ANTLR(reader.read())
            return arith.tree(expr, 's')

    def ptree2ast(self, ptree, simple=True):
        ast = self._atw_ptree_to_ast(ptree)
        if simple: ast = self._atw_ast_simpler(ast)
        return ast

    def shuntingYardExpr2ast(self, expr, simple=True):
        ast = self._shunting_yard_parser.parse(expr)
        if simple: ast = self._atw_ast_simpler(ast)
        return ast

    def blocks(self, ast):
        return self._atw_block_generator.start(ast)

    def prior(self, ast):
        return self._atw_block_priority.start(ast)

    def eval(self, ast, memory=None):
        if memory is None:
            memory = dict()
        return self._atw_eval_expr.start(ast, memory)

    def latex(self, ast, memory):
        return self._atw_latex_formatter.start(ast, memory)
