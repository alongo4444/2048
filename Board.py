import threading

import Tile
import random
from playsound import playsound

class Board:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board_arr = self.initialize_board(board_size)
        self.board_tiles = [[0] * board_size for i in range(board_size)]
        self.update_tiles(self.board_arr)

    def load_board(self,arr, board_size):
        self.board_size = board_size
        self.board_arr = arr
        self.board_tiles = [[0] * board_size for i in range(board_size)]
        self.update_tiles(self.board_arr)

    def update_tiles(self, arr):
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                self.board_tiles[i][j] = Tile.Tile(arr[i][j], i, j)

    def move_board_up(self):

        changed = False
        # move all
        for j in range(len(self.board_arr[0])):
            for i in range(1, len(self.board_arr), 1):
                if self.board_arr[i][j] != 0:
                    counter = i - 1
                    while (counter > -1 and self.board_arr[counter][j] == 0):
                        counter = counter - 1
                    self.board_arr[counter + 1][j] = self.board_arr[i][j]
                    if i - counter != 1:
                        changed = True
                        self.board_arr[i][j] = 0

        # merge
        for j in range(len(self.board_arr[0])):
            for i in range(len(self.board_arr) - 1):
                if self.board_arr[i][j] != 0 and self.board_arr[i][j] == self.board_arr[i + 1][j]:
                    changed = True
                    self.board_arr[i][j] = self.board_arr[i][j] + self.board_arr[i + 1][j]
                    for k in range(i + 1, len(self.board_arr) - 1, 1):
                        self.board_arr[k][j] = self.board_arr[k + 1][j]
                    self.board_arr[len(self.board_arr) - 1][j] = 0

        if changed:
            self.play_sound_move()
            self.generate_new_tile()
        else:
            self.play_sound_no_move()
        return self.check_valid_moves()

    def move_board_down(self):
        changed = False
        # move all
        for j in range(len(self.board_arr[0])):
            for i in range(len(self.board_arr) - 2, -1, -1):
                if (self.board_arr[i][j] != 0):
                    counter = i + 1
                    while counter < self.board_size and self.board_arr[counter][j] == 0:
                        counter = counter + 1
                    self.board_arr[counter - 1][j] = self.board_arr[i][j]
                    if (counter - i != 1):
                        changed = True
                        self.board_arr[i][j] = 0

        # merge
        for j in range(len(self.board_arr[0])):
            for i in range(len(self.board_arr) - 1, 0, -1):
                if self.board_arr[i][j] != 0 and self.board_arr[i][j] == self.board_arr[i - 1][j]:
                    self.board_arr[i][j] = self.board_arr[i][j] + self.board_arr[i - 1][j]
                    changed = True
                    for k in range(i - 1, 0, -1):
                        self.board_arr[k][j] = self.board_arr[k - 1][j]
                    self.board_arr[0][j] = 0

        if changed:
            self.play_sound_move()
            self.generate_new_tile()
        else:
            self.play_sound_no_move()
        return self.check_valid_moves()

    def move_board_right(self):
        changed = False
        # move all
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0]) - 2, -1, -1):
                if self.board_arr[i][j] != 0:
                    counter = j + 1
                    while counter < self.board_size and self.board_arr[i][counter] == 0:
                        counter = counter + 1
                    self.board_arr[i][counter - 1] = self.board_arr[i][j]
                    if counter - j != 1:
                        changed = True
                        self.board_arr[i][j] = 0

        # merge
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0]) - 1, 0, -1):
                if self.board_arr[i][j] != 0 and self.board_arr[i][j] == self.board_arr[i][j - 1]:
                    changed = True
                    self.board_arr[i][j] = self.board_arr[i][j] + self.board_arr[i][j - 1]
                    for k in range(j - 1, 0, -1):
                        self.board_arr[i][k] = self.board_arr[i][k - 1]
                    self.board_arr[i][0] = 0

        if changed:
            self.play_sound_move()
            self.generate_new_tile()
        else:
            self.play_sound_no_move()
        return self.check_valid_moves()

    def move_board_left(self):
        changed = False
        # move all
        for i in range(len(self.board_arr)):
            for j in range(1, len(self.board_arr[0]), 1):
                if (self.board_arr[i][j] != 0):
                    counter = j - 1
                    while (counter > -1 and self.board_arr[i][counter] == 0):
                        counter = counter - 1
                    self.board_arr[i][counter + 1] = self.board_arr[i][j]
                    if (j - counter != 1):
                        changed = True
                        self.board_arr[i][j] = 0

        # merge
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0]) - 1):
                if (self.board_arr[i][j] != 0 and self.board_arr[i][j] == self.board_arr[i][j + 1]):
                    changed = True
                    self.board_arr[i][j] = self.board_arr[i][j] + self.board_arr[i][j + 1]
                    for k in range(j + 1, len(self.board_arr[0]) - 1, 1):
                        self.board_arr[i][k] = self.board_arr[i][k + 1]
                    self.board_arr[i][len(self.board_arr[0]) - 1] = 0

        if changed:
            self.play_sound_move()
            self.generate_new_tile()
        else:
            self.play_sound_no_move()
        return self.check_valid_moves()

    def print_board(self):
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0])):
                print(self.board_arr[i][j], end="")
                print("|", end="")
            print("")

    def initialize_board(self, board_size):
        arr = [[0] * board_size for i in range(board_size)]
        i1 = random.randint(0, board_size - 1)
        j1 = random.randint(0, board_size - 1)
        i2 = i1
        j2 = j1
        while i1 == i2 and j1 == j2:
            i2 = random.randint(0, board_size - 1)
            j2 = random.randint(0, board_size - 1)
        for i in range(board_size):
            for j in range(board_size):
                if i == i1 and j == j1 or i == i2 and j == j2:
                    arr[i][j] = 2 * random.randint(1, 2)
                else:
                    arr[i][j] = 0
        return arr

    def get_empty_tiles(self):
        empty_indexes = []
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0])):
                if self.board_arr[i][j] == 0:
                    pair = (i, j)
                    empty_indexes.append(pair)
        return empty_indexes

    def generate_new_tile(self):
        empty_indexes = self.get_empty_tiles()
        if len(empty_indexes) > 0:
            i = random.randint(0, len(empty_indexes) - 1)
            x, y = empty_indexes.pop(i)
            self.board_arr[x][y] = 2 * random.randint(1, 2)

    def check_valid_moves(self):
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0])):
                if self.board_arr[i][j] == 0:
                    return True
        # check rows
        for i in range(len(self.board_arr)):
            for j in range(len(self.board_arr[0]) - 1):
                if self.board_arr[i][j] == self.board_arr[i][j + 1]:
                    return True
        # check cols
        for i in range(len(self.board_arr) - 1):
            for j in range(len(self.board_arr[0])):
                if self.board_arr[i][j] == self.board_arr[i + 1][j]:
                    return True
        sound_thread = threading.Thread(target=lambda: playsound('Sounds/fail.wav'))
        sound_thread.start()
        return False

    def play_sound_move(self):
        sound_thread = threading.Thread(target=lambda: playsound('Sounds/boop.wav'))
        sound_thread.start()

    def play_sound_no_move(self):
        sound_thread = threading.Thread(target=lambda: playsound('Sounds/tap.wav'))
        sound_thread.start()


if (False):
    b = Board([[2, 4, 8, 0],
               [0, 4, 4, 2],
               [2, 2, 0, 8],
               [2, 2, 4, 0]])
    b.print_board()
    print("")
    print("Move Right:")
    b.move_board_right()
    b.print_board()
    print("")
    print("Move Right:")
    b.move_board_right()
    b.print_board()
    print("")
    print("Move Up:")
    b.move_board_up()
    b.print_board()
    b.update_tiles(b.board_arr)
    c = b.board_tiles[0][2].getColor()
