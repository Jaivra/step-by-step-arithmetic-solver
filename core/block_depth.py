import itertools

from core.MalformedExpression import MalformedExpression


class BLOCK_TYPE:
    ROUND = 3
    SQUARE = 2
    CURLY = 1
    INIT = 0

class PARENTH_TYPE:
    SIMPLE = 0
    FREE = 1

class BlockDepth:

    _count = itertools.count(0)


    def __init__(self, block_type=BLOCK_TYPE.INIT, depth=0, pos=0):
        self._block_type = block_type
        self._depth = depth
        self._pos = pos



    def add_block(self, block_type):
        def block_type_to_str(block_type):
            TAB = {BLOCK_TYPE.ROUND: 'Tonda',
                   BLOCK_TYPE.SQUARE: 'Quadra',
                   BLOCK_TYPE.CURLY: 'Graffa',
                   }
            return TAB[block_type]

        depth = self._depth
        if self._block_type == block_type == BLOCK_TYPE.ROUND:
            depth += 1
        elif self._block_type >= block_type:
            raise MalformedExpression(
                'Errore nell\'annidamento delle parentesi, regole di parentesizzazione non rispettate, ' +
                'non puoi inserire una parentesi ' + block_type_to_str(block_type) + ' in una parentesi ' + block_type_to_str(self._block_type),
                [],
                [],
                []
            )

        return BlockDepth(block_type, depth, next(BlockDepth._count))

    @property
    def block_type(self):
        return self._block_type

    @property
    def depth(self):
        return self._depth

    @property
    def pos(self):
        return self._pos

    def __gt__(self, other):
        return self._block_type > other.block_type or \
               (self._block_type == other.block_type and self._depth > other.depth) or \
               (self._block_type == other.block_type and self._depth == other.depth and self._pos < other.pos)

    def __repr__(self):
        return f'{self._block_type}{self._depth}{self._pos}'
