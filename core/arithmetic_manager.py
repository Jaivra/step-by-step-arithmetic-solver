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
        domain_checker = create_domain_checker(
            domain)  # Crea la funzione per valutare l'appartenenza di un valore al dominio *domain* passato in input
        self._atw_ast_simpler = AtwAstSimpler(domain_checker)
        self._shunting_yard_parser = ShuntingYardParser()
        self._atw_block_generator = AtwBlockGenerator()
        self._atw_latex_formatter = AtwLatexFormatter()
        self._atw_block_priority = AtwBlockPriority()
        self._atw_eval_expr = AtwEvalExpr(domain_checker)

    """ 
    Riceve in input un'espressione e genera l'AST utilizzando l'algoritmo Shunting-Yard
    restituisce l'AST corrispondente applicando alcune semplificazioni
    """
    def shuntingYardExpr2ast(self, expr):
        ast = self._shunting_yard_parser.parse(expr)
        ast = self._atw_ast_simpler(ast)
        return ast

    """
    Riceve in input un AST e restituisce una lista di AST, ognuno dei quali corrisponde ad una sottoespressione.
    La lista restituita sarà ordinata secondo il grado di annidamento delle espressioni e quindi secondo l'ordine di valutazione.
    """
    def blocks(self, ast):
        return self._atw_block_generator.start(ast)

    """
    Riceve un AST/blocco in input, annota la priorità di ogni nodo a seconda della priorità dell'operazione corrispondente.
    Restituisce il parent del nodo che dovrà essere calcolato nel prossimo step di valutazione.
    """
    def prior(self, ast):
        return self._atw_block_priority.start(ast)

    """ 
    Riceve un AST in input e lo valuta, MEMORY è un dizionario che contiene i valori delle espressioni precedentemente calcolate
    """
    def eval(self, ast, memory=None):
        if memory is None:
            memory = dict()
        res = self._atw_eval_expr.start(ast, memory)
        return res

    """
    Riceve un AST in input e stampa l'espressione secondo il formato definito in Latex
    """
    def latex(self, ast, memory):
        return self._atw_latex_formatter.start(ast, memory)
