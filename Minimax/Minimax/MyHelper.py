import math

def get_new_children(grid):
    possible_moves = [0, 1, 2, 3]
    new_children = []
    moving = []
    for each_move in possible_moves:
        grid_copy = list(grid)
        has_moved = apply_move(grid_copy, each_move)
        if has_moved:
            new_children.append(grid_copy)
            moving.append(each_move)
    return [new_children, moving]

def combine_cells(cells):
    if len(cells) <= 1:
        return cells
    count = 0
    while count < len(cells) - 1:
        if cells[count] == cells[count + 1]:
            cells[count] *= 2
            del cells[count + 1]
        count += 1

def apply_move(grid, direction):
    has_moved = False
    if direction == 0:
        for i in range(4):
            cells = []
            for j in range(i, i + 13, 4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            combine_cells(cells)
            for j in range(i, i + 13, 4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    has_moved = True
                grid[j] = value
        return has_moved
    elif direction == 1:
        for i in range(4):
            cells = []
            for j in range(i + 12, i - 1, -4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            combine_cells(cells)
            for j in range(i + 12, i - 1, -4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    has_moved = True
                grid[j] = value
        return has_moved
    elif direction == 2:
        for i in [0, 4, 8, 12]:
            cells = []
            for j in range(i, i + 4):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            combine_cells(cells)
            for j in range(i, i + 4):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    has_moved = True
                grid[j] = value
        return has_moved
    elif direction == 3:
        for i in [3, 7, 11, 15]:
            cells = []
            for j in range(i, i - 4, -1):
                cell = grid[j]
                if cell != 0:
                    cells.append(cell)
            combine_cells(cells)
            for j in range(i, i - 4, -1):
                value = cells.pop(0) if cells else 0
                if grid[j] != value:
                    has_moved = True
                grid[j] = value
        return has_moved

def is_valid_move(grid):
    if 0 in grid:
        return True
    for i in range(16):
        if (i + 1) % 4 != 0:
            if grid[i] == grid[i + 1]:
                return True
        if i < 12:
            if grid[i] == grid[i + 4]:
                return True
    return False

def calculate_heuristic(grid):
    empty_tiles = len([i for i, x in enumerate(grid) if x == 0])
    highest_tile = max(grid)
    order = 0
    weights = [65536, 32768, 16384, 8192, 512, 1024, 2048, 4096, 256, 128, 64, 32, 2, 4, 8, 16]
    if highest_tile == grid[0]:
        order += (math.log(grid[0]) / math.log(2)) * weights[0]
    for i in range(16):
        if grid[i] >= 8:
            order += weights[i] * (math.log(grid[i]) / math.log(2))
            return order / (16 - empty_tiles)

    main_grid = [[0] * 4 for i in range(4)]
    k = 0
    for i in range(4):
        for j in range(4):
            main_grid[i][j] = grid[k]
            k += 1
    sum_diff = 0
    for i in range(4):
        for j in range(4):
            if main_grid[i][j] != 0:
                val = math.log(main_grid[i][j]) / math.log(2)
                for k in range(3 - j):
                    next_right = main_grid[i][j + k + 1]
                    if next_right != 0:
                        right_val = math.log(next_right) / math.log(2)
                        if right_val != val:
                            sum_diff -= math.fabs(right_val - val)
                            break
                for k in range(3 - i):
                    next_down = main_grid[i + k + 1][j]
                    if next_down != 0:
                        down_val = math.log(next_down) / math.log(2)
                        if down_val != val:
                            sum_diff -= math.fabs(down_val - val)
                            break
    min_diff = 0
    up_diff = 0
    down_diff = 0
    left_diff = 0
    right_diff = 0
    for i in range(4):
        j = 0
        k = j + 1
        while k < 4:
            if main_grid[i][k] == 0:
                k += 1
            else:
                if main_grid[i][j] == 0:
                    curr = 0
                else:
                    curr = math.log(main_grid[i][j]) / math.log(2)
                next_val = math.log(main_grid[i][k]) / math.log(2)
                if curr > next_val:
                    up_diff += next_val - curr
                elif next_val > curr:
                    down_diff += curr - next_val
            j = k
            k += 1
    for j in range(4):
        i = 0
        k = i + 1
        while k < 4:
            if main_grid[j][k] == 0:
                k += 1
            else:
                if main_grid[j][i] == 0:
                    curr = 0
                else:
                    curr = math.log(main_grid[j][i]) / math.log(2)
                next_val = math.log(main_grid[j][k]) / math.log(2)
                if curr > next_val:
                    left_diff += next_val - curr
                elif next_val > curr:
                    right_diff += curr - next_val
            i = k
            k += 1
    net_diff = max(up_diff, down_diff) + max(left_diff, right_diff)
    return 0.1 * sum_diff + min_diff + math.log(highest_tile) / math.log(2) + empty_tiles
