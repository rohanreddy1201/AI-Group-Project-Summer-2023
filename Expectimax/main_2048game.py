from ai import AI
from game_board import GameBoard
from random import randint, seed
import numpy as np

dirs = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}
# python main_cli > output.txt

stepValue_256Array = []
stepValue_512Array = []
stepValue_1024Array = []
stepValue_2048Array = []
stepValue_4096Array = []
game_max_values = []
total_games = 50

class CLIRunner:
    def __init__(self):
        self.board = GameBoard()
        self.ai = AI()

        self.init_game()
        # self.print_game_board()

        self.run_game()

        self.over = False

    def init_game(self):
        self.insert_random_tile()
        self.insert_random_tile()


    def check_value(self, param):
        elem_to_find = param
        return any(elem_to_find in sub_list for sub_list in self.board.grid)

    """
    In this scenario player is trying to find the solution of the game using merging technique 
    to the tiles together by applying the best move
    Here computer is trying to insert random tiles at any random location
    """
    def run_game(self):
        turn_gamecount = 0
        step_countfor_256 = 0
        step_countfor_512 = 0
        step_countfor_1024 = 0
        step_countfor_2048 = 0
        step_countfor_4096 = 0
        while True:
            turn_gamecount += 1
            move = self.ai.get_move(self.board)
            self.board.move(move)
            self.insert_random_tile()

            if step_countfor_256 == 0 and self.check_value(256):
                step_countfor_256 = turn_gamecount
            if step_countfor_512 == 0 and self.check_value(512):
                step_countfor_512 = turn_gamecount
            if step_countfor_1024 == 0 and self.check_value(1024):
                step_countfor_1024 = turn_gamecount
            if step_countfor_2048 == 0 and self.check_value(2048):
                step_countfor_2048 = turn_gamecount
            if step_countfor_4096 == 0 and self.check_value(4096):
                step_countfor_4096 = turn_gamecount

            if len(self.board.get_available_moves()) == 0:
                print("- Game is Over (max tile / max score): " + str(self.board.get_max_tile()))
                game_max_values.append(self.board.get_max_tile())
                self.print_game_board()
                break

        stepValue_256Array.append(step_countfor_256)
        stepValue_512Array.append(step_countfor_512)
        stepValue_1024Array.append(step_countfor_1024)
        stepValue_2048Array.append(step_countfor_2048)
        stepValue_4096Array.append(step_countfor_4096)

        if step_countfor_2048 != 0:
            print("-***** GAME WON!!!!! *****-")
            print("-***** Steps taken to reach 1st 2048: ", step_countfor_2048)
            print("")
        else:
            print("-***** GAME LOST!!!!! *****-")
            print("-***** NO 2048 *****-")
            print("")

    """
    We are here printing the 4 X 4 board / grid
    """
    def print_game_board(self):
        for i in range(4):
            for j in range(4):
                print("%6d  " % self.board.grid[i][j], end="")
            print("")
        print("")

    """
    This function is useful and helps us to insert random 2 tiles at any different location 
    Values we are taking as 2 or 4 initially
    """
    def insert_random_tile(self):
        if randint(0,99) < 100 * 0.9:
            value = 2
        else:
            value = 4

        cells = self.board.get_available_cells()
        pos = cells[randint(0, len(cells) - 1)] if cells else None

        if pos is None:
            return None
        else:
            self.board.insert_tile(pos, value)
            return pos


def save_to_file(fileName, arrayValue):
    a_file = open(fileName, "w")
    np.savetxt(a_file, arrayValue, delimiter=',')
    a_file.close()


if __name__ == '__main__':
    for i in range(total_games):
        print("------ Game Counts: ",i+1,"------")
        CLIRunner()

    save_to_file("step256.txt", stepValue_256Array)
    save_to_file("step512.txt", stepValue_512Array)
    save_to_file("step1024.txt", stepValue_1024Array)
    save_to_file("step2048.txt", stepValue_2048Array)
    save_to_file("maxValuesList.txt", game_max_values)
