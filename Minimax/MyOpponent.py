from random import randint

class MyOpponent:
    def get_move(self, grid):
        c = grid.get_empty_cells()
        if c:
            return c[randint(0, len(c) - 1)]
        else:
            return None
