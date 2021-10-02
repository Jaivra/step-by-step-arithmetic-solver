from liblet import ANTLR

from core.atw_ast_simpler import AtwAstSimpler
from core.atw_block_generator import AtwBlockGenerator
from core.atw_latex_formatter import AtwLatexFormatter
from core.atw_expr_eval import AtwEvalExpr
from core.atw_block_priority import AtwBlockPriority
from core.shunting_yard_parser import ShuntingYardParser
from core.util import *


class ArithManager:

    def __init__(self, domain):
        domain_checker = create_domain_checker(domain)
        self._atw_ast_simpler = AtwAstSimpler(domain_checker)
        self._shunting_yard_parser = ShuntingYardParser()
        self._atw_block_generator = AtwBlockGenerator()
        self._atw_latex_formatter = AtwLatexFormatter()
        self._atw_block_priority = AtwBlockPriority()
        self._atw_eval_expr = AtwEvalExpr(domain_checker)


    # Prende in input un'espressione e restituisce l'ast attraverso l'algoritmo Shunting-Yard
    def shuntingYardExpr2ast(self, expr, simple=True):
        ast = self._shunting_yard_parser.parse(expr)
        if simple: ast = self._atw_ast_simpler(ast)
        return ast

    # prende in input un'AST e trova e restituisce una lista di blocchi con priorità (che si riferiscono alle sottoespressioni) secondo l'ordine di esecuzione
    def blocks(self, ast):
        return self._atw_block_generator.start(ast)

    # Riceve un blocco in input e restituisce il parent del nodo che deve essere calcolato, ridefinendo la priorità del blocco in questione
    def prior(self, ast):
        return self._atw_block_priority.start(ast)


    # Riceve un blocco in input e lo valuta, memory è un dizionario che contiene i valori degli altri blocchi già calcolati
    def eval(self, ast, memory=None):
        if memory is None:
            memory = dict()
        res = self._atw_eval_expr.start(ast, memory)
        return res

    # Riceve un'AST in input e stampa l'espressione in Latex
    def latex(self, ast, memory):
        return self._atw_latex_formatter.start(ast, memory)
