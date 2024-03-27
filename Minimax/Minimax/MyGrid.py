from copy import deepcopy

directions = (UP_DIR, DOWN_DIR, LEFT_DIR, RIGHT_DIR) = ((-1, 0), (1, 0), (0, -1), (0, 1))
dir_index = [UP, DOWN, LEFT, RIGHT] = range(4)

class MyGrid:
    def __init__(self, size=4):
        self.size = size
        self.map = [[0] * self.size for _ in range(self.size)]

    def copying(self):
        temp = MyGrid()
        temp.map = deepcopy(self.map)
        temp.size = self.size
        return temp

    def insert_tile(self, pos, value):
        self.set_cell_value(pos, value)

    def set_cell_value(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    def get_empty_cells(self):
        cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 0:
                    cells.append((i, j))
        return cells

    def get_highest_tile(self):
        highest_value_cell = 0
        for i in range(self.size):
            for j in range(self.size):
                highest_value_cell = max(highest_value_cell, self.map[i][j])
        return highest_value_cell

    def check_insertion(self, pos):
        return self.get_cell_value(pos) == 0

    def move(self, direction):
        direction = int(direction)
        if direction == UP:
            return self.move_up_or_down(False)
        if direction == DOWN:
            return self.move_up_or_down(True)
        if direction == LEFT:
            return self.move_left_or_right(False)
        if direction == RIGHT:
            return self.move_left_or_right(True)

    def move_up_or_down(self, down):
        r = range(self.size - 1, -1, -1) if down else range(self.size)
        is_moved = False
        for j in range(self.size):
            cells = []
            for i in r:
                cell = self.map[i][j]
                if cell != 0:
                    cells.append(cell)
            self.combine(cells)
            for i in r:
                value = cells.pop(0) if cells else 0
                if self.map[i][j] != value:
                    is_moved = True
                self.map[i][j] = value
        return is_moved

    def move_left_or_right(self, right):
        r = range(self.size - 1, -1, -1) if right else range(self.size)
        is_moved = False
        for i in range(self.size):
            cells = []
            for j in r:
                cell = self.map[i][j]
                if cell != 0:
                    cells.append(cell)
            self.combine(cells)
            for j in r:
                value = cells.pop(0) if cells else 0
                if self.map[i][j] != value:
                    is_moved = True
                self.map[i][j] = value
        return is_moved

    def combine(self, cells):
        if len(cells) <= 1:
            return cells
        count = 0
        while count < len(cells) - 1:
            if cells[count] == cells[count + 1]:
                cells[count] *= 2
                del cells[count + 1]
            count += 1

    def check_if_move(self, dirs=dir_index):
        check_possible_moves = set(dirs)

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y]:
                    for i in check_possible_moves:
                        possible_move = directions[i]
                        adj_value = self.get_cell_value((x + possible_move[0], y + possible_move[1]))
                        if adj_value == self.map[x][y] or adj_value == 0:
                            return True
                elif self.map[x][y] == 0:
                    return True
        return False

    def get_possible_moves(self, dirs=dir_index):
        possible_moves = []
        for x in dirs:
            temp = self.copying()
            if temp.move(x):
                possible_moves.append(x)
        return possible_moves

    def cross_bound(self, pos):
        return pos[0] < 0 or pos[0] >= self.size or pos[1] < 0 or pos[1] >= self.size

    def get_cell_value(self, pos):
        if not self.cross_bound(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None

if __name__ == '__main__':
    g = MyGrid()
    g.map[0][0] = 2
    g.map[2][0] = 4
    while True:
        for i in g.map:
            print(i)
        print(g.get_possible_moves())
        v = input()
        g.move(v)
