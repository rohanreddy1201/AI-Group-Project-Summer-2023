import numpy as np
import MyHelper

def calculate(grid, d, isMax):
    if d == 0:
        return MyHelper.h(grid)
    if not MyHelper.vM(grid):
        return MyHelper.h(grid)
    if isMax:
        best = -np.inf
        [c, _] = MyHelper.gC(grid)
        for ch in c:
            best = max(best, calculate(ch, d - 1, False))
        return best
    else:
        cells = [i for i, x in enumerate(grid) if x == 0]
        c = []
        best = np.inf
        for cell in cells:
            temp = list(grid)
            temp[cell] = 2
            c.append(temp)
            temp = list(grid)
            temp[cell] = 4
            c.append(temp)
        for ch in c:
            best = min(best, calculate(ch, d - 1, True))
        return best
