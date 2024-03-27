import MyHelper
import numpy as np

def calculate(grid, depth, alpha, beta, isMax):
    if depth == 0:
        return MyHelper.calculate_heuristic(grid)
    if not MyHelper.is_valid_move(grid):
        return MyHelper.calculate_heuristic(grid)
    if isMax:
        best = -np.inf
        [c,m] = MyHelper.get_new_children(grid)
        for ch in c:
            best = max(best, calculate(ch, depth - 1, alpha, beta, False))
            if best >= beta:
                return best
            alpha = max(alpha, best)
        return best
    else:
        cells = [i for i, x in enumerate(grid) if x == 0]
        c = []
        for cell in cells:
            temp = list(grid)
            temp[cell] = 2
            c.append(temp)
            temp = list(grid)
            temp[cell] = 4
            c.append(temp)
        best = np.inf
        for ch in c:
            best = min(best, calculate(ch, depth - 1, alpha, beta, True))
            if best <= alpha:
                return best
            beta = min(beta, best)
        return best
