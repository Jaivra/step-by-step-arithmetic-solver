import re
import warnings


from fractions import Fraction

from liblet import Tree


class MyAtw:

    def __init__(self, key):
        self._key = key

        methods_to_register = [method_name for method_name in dir(self)
                               if callable(getattr(self, method_name))
                               and re.match(r'_atw_[^\W\d_]+', method_name)]
        self._dispatch_table = {method[5:]:getattr(self, method) for method in methods_to_register}

        self.key = key

    def catchall(self, tree):
        warnings.warn('TREE_CATCHALL: {}'.format(tree.root))
        trees = []
        for child in tree.children:
            t = self(child)
            if t is not None: trees.append(t)
        return Tree(tree.root, trees)


    def __call__(self, tree):
        key = tree.root[self._key]
        return self._dispatch_table[key](tree) if key in self._dispatch_table else self.catchall(tree)
