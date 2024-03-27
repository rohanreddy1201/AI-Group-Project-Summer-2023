import MyMinimax
import MyAlphaBetaPrune
from MyGrid import MyGrid
import numpy as np
import MyHelper

class MyPlayer:
    def get_move(self, grid):
        copy_grid = [val for row in grid.map for val in row]
        [child, moves] = MyHelper.get_new_children(copy_grid)
        max_path = -np.inf
        direction = 0
        for i in range(len(child)):
            c = child[i]
            m = moves[i]
            highest_value = -np.inf
            max_depth = 4
            highest_value = MyAlphaBetaPrune.calculate(c, max_depth, -np.inf, np.inf, False)
            if m == 0 or m == 2:
                highest_value += 10000
            if highest_value > max_path:
                direction = m
                max_path = highest_value
        return direction

if __name__ == '__main__':
    agent = MyPlayer()
    g = MyGrid()
    g.map[0][0] = 2
    g.map[2][0] = 4
    while True:
        value = agent.get_move(g)
        g.move(value)
