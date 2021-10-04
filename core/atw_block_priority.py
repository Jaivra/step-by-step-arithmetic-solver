from core.config import PRIORITY
from core.my_atw import MyAtw
from core.util import *


""" 
Classe che dato un AST, restituisce il parent del nodo che rappresenta l'espressione da calcolare nel prossimo step.
Inoltre ricalcola e annota l'AST ricevuto in input con le nuove priorità delle operazioni senza tenere conto della prossima operazione da calcolare.
"""
class AtwBlockPriority(MyAtw):
    def __init__(self):
        super().__init__('type')

    def start(self, ast):
        return self(ast)

    def _atw_atomExpr(self, ast):
        return None

    def _atw_subExpr(self, ast):
        return None

    # Gestione delle espressioni binarie
    def _arithExpr(self, ast):
        if is_calculable(ast): # Verifica se è possibile calcolare l'operazione, nel caso in cui i figli sono atom o sottoespressioni già calcolate
            ast.root['_calc'] = 'next'
            ast.root['priority'] = 0
            return None # Deve restituire il padre del nodo da calcolare, quindi per ora sarà None

        left, right = ast.children
        # Calcola la priorità maggiore dei figli per capire dove proseguire con la visita, è inutile visitare tutta la sottoespressione,
        # visitiamo solo il cammino che contiene la prossima operazione da calcolare
        if left.root['priority'] >= right.root['priority']:
            par = self(left)
        else:
            par = self(right)

        # Caso in cui il nodo corrente sia il padre della prossima operazione da calcolare
        if is_next_to_calc(left) or is_next_to_calc(right):
            return ast
        return par

    def _atw_addSubExpr(self, ast):
        par = self._arithExpr(ast)

        left, right = ast.children
        child_types = set(child.root['type'] for child in ast.children)

        ast.root['priority'] = max(PRIORITY['addSubExpr'], left.root['priority'], right.root['priority'])

        # Necessario nel caso in cui la sottoespressione da calcolare è una somma/sottrazione
        # e il padre della sottoespressione è il nodo corrente,
        # in questo caso dobbiamo svolgere tutte le operazioni in un solo passo
        if 'addSubExpr' in child_types and child_types & {'subExpr', 'atomExpr'}:
            if is_next_to_calc(left):
                del left.root['_calc']
                ast.root['_calc'] = 'next'
                ast.root['priority'] = 0
            elif is_next_to_calc(right):
                del right.root['_calc']
                ast.root['_calc'] = 'next'
                ast.root['priority'] = 0
        return par

    def _atw_divProdExpr(self, ast):
        par = self._arithExpr(ast)

        left, right = ast.children
        child_types = set(child.root['type'] for child in ast.children)

        if not is_next_to_calc(ast):
            ast.root['priority'] = max(PRIORITY['divProdExpr'], left.root['priority'], right.root['priority'])

        # Necessario nel caso in cui la sottoespressione da calcolare è un prodotto/divisione
        # e il padre della sottoespressione è il nodo corrente,
        # in questo caso dobbiamo svolgere tutte le operazioni in un solo passo
        if 'divProdExpr' in child_types and child_types & {'subExpr', 'atomExpr'}:
            if is_next_to_calc(left):
                del left.root['_calc']
                ast.root['_calc'] = 'next'
                ast.root['priority'] = 0
            elif is_next_to_calc(right):
                del right.root['_calc']
                ast.root['_calc'] = 'next'
                ast.root['priority'] = 0
        return par

    def _atw_powExpr(self, ast):
        par = self._arithExpr(ast)
        if not is_next_to_calc(ast):
            ast.root['priority'] = max(PRIORITY['powExpr'], ast.children[0].root['priority'])
        return par

    def _atw_unaryExpr(self, ast):
        if is_calculable(ast):
            ast.root['_calc'] = 'next'
            ast.root['priority'] = 0
            return None
        par = self(ast.children[0])
        ast.root['priority'] = max(PRIORITY['unaryExpr'], ast.children[0].root['priority'])

        if is_next_to_calc(ast.children[0]):
            return ast
        return par

    def _atw_fractExpr(self, ast):
        par = self._arithExpr(ast)
        if not is_next_to_calc(ast):
            ast.root['priority'] = max(PRIORITY['fractExpr'], ast.children[0].root['priority'])
        return par

    def _container(self, ast):
        par = self(ast.children[0])
        if is_next_to_calc(ast.children[0]):
            return ast
        return par

    def _atw_main(self, ast):
        return self._container(ast)

    def _atw_roundBlockExpr(self, ast):
        return self._container(ast)

    def _atw_squareBlockExpr(self, ast):
        return self._container(ast)

    def _atw_curlyBlockExpr(self, ast):
        return self._container(ast)
