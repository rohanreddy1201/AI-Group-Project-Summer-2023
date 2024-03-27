from MyGrid import MyGrid
from MyOpponent import MyOpponent
from MyPlayer import MyPlayer
from random import randint
import time
import matplotlib.pyplot as plt
import numpy as np

initial_tiles = 2
(agent, opponent) = (0, 1)
possible_directions = {0: "UP", 1: 'DOWN', 2: 'LEFT', 3: 'RIGHT'}
time_limit = 1
probability = 0.9
max_tiles_array = []


class Game2048:
    def __init__(self, size=4):
        self.grid = MyGrid(size)
        self.possible_tile_value = [2, 4]
        self.prob = probability
        self.initial_tiles = initial_tiles
        self.opponent = None
        self.agent = None
        self.end = False

    def set_agent(self, agent):
        self.agent = agent

    def set_opponent(self, opponent):
        self.opponent = opponent

    def set_clock(self, time):
        if time - self.prev_time > time_limit + 0.1:
            self.end = True
        else:
            self.prev_time = time

    def is_game_completed(self):
        return not self.grid.check_if_move()

    def insert_random_tile(self):
        tile = self.get_next_tile()
        cells = self.grid.get_empty_cells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.set_cell_value(cell, tile)

    def get_next_tile(self):
        if randint(0, 99) < 100 * self.prob:
            return self.possible_tile_value[0]
        else:
            return self.possible_tile_value[1]

    def start(self):
        for i in range(self.initial_tiles):
            self.insert_random_tile()

        self.display(self.grid)

        turn = agent
        highest_tile = 0

        self.prev_time = time.perf_counter()

        while not self.is_game_completed() and not self.end:
            temp = self.grid.copying()
            move = None

            if turn == agent:
                print("Agent is playing")
                move = self.agent.get_move(temp)

                if move is not None and 0 <= move < 4:
                    if self.grid.check_if_move([move]):
                        self.grid.move(move)
                        highest_tile = self.grid.get_highest_tile()
                    else:
                        print("Wrong Move")
                        self.end = True
                else:
                    print("Wrong Move - 1")
                    self.end = True
            else:
                print("Opponent is playing")
                move = self.opponent.get_move(temp)
                if move and self.grid.check_insertion(move):
                    self.grid.set_cell_value(move, self.get_next_tile())
                else:
                    print("Wrong move")
                    self.end = True

            if not self.end:
                self.display(self.grid)
            self.set_clock(time.perf_counter())
            turn = 1 - turn
        max_tiles_array.append(highest_tile)
        print("Highest Score for this game:", highest_tile)

    def display(self, grid):
        for i in range(grid.size):
            for j in range(grid.size):
                print("%6d  " % grid.map[i][j], end="")
            print("")
        print("")
        print("")


def main():
    game = Game2048()
    agent = MyPlayer()
    opponent = MyOpponent()
    game.set_agent(agent)
    game.set_opponent(opponent)
    game.start()


if __name__ == '__main__':
    num_iterations = 50
    for i in range(num_iterations):
        print("--------------------------Iteration :", i + 1, "--------------------------------------")
        main()
    powers_of_2 = [32, 64, 128, 256, 512, 1024, 2048]
    y = []
    my_labels = []
    print("Max tiles array", max_tiles_array)
    for i in range(len(powers_of_2)):
        if max_tiles_array.count(powers_of_2[i]) != 0:
            y.append(max_tiles_array.count(powers_of_2[i]))
            my_labels.append(
                str(powers_of_2[i]) + '\n' + str((max_tiles_array.count(powers_of_2[i]) / num_iterations) * 100) + "%")
    result = np.array(y)
    print('Result', result)
    print('Labels', my_labels)
    print("Percentage of 32's", (max_tiles_array.count(32) / num_iterations) * 100)
    print("Percentage of 64's", (max_tiles_array.count(64) / num_iterations) * 100)
    print("Percentage of 128's", (max_tiles_array.count(128) / num_iterations) * 100)
    print("Percentage of 256's", (max_tiles_array.count(256) / num_iterations) * 100)
    print("Percentage of 512's", (max_tiles_array.count(512) / num_iterations) * 100)
    print("Percentage of 1024's", (max_tiles_array.count(1024) / num_iterations) * 100)
    print("Percentage of 2048's", (max_tiles_array.count(2048) / num_iterations) * 100)
    plt.pie(result, labels=my_labels)
    plt.title("Percentage of Occurrences:")

    plt.show()
