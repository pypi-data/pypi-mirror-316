import numpy as np

class Sudoku:
    def __init__(self, board):
        self.board = board

    def is_valid(self, row, col, num):
        return (num not in self.board[row] and
                num not in self.board[:, col] and
                num not in self.board[3 * (row // 3):3 * (row // 3) + 3,
                           3 * (col // 3):3 * (col // 3) + 3])

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r, c] == 0:
                    return r, c
        return None

    def solve(self):
        empty_cell = self.find_empty()
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row, col] = num
                if self.solve():
                    return True
                self.board[row, col] = 0  # возрат назад

        return False

    def print_board(self):
        print("\n".join(" ".join(map(str, row)) for row in self.board))

    def analyze(self):
        if np.count_nonzero(self.board) < 17:
            print("Мало чисел для решения судоку")
            return

        if self.solve():
            print("Судоку решено:)")
            self.print_board()
        else:
            print("Судоку невозможно решать:(")

initial_board = np.array([
    [5, 0, 0, 4, 0, 7, 9, 0, 3],
    [0, 0, 2, 0, 1, 0, 0, 8, 7],
    [1, 0, 0, 6, 8, 0, 0, 0, 4],
    [8, 0, 0, 3, 0, 0, 7, 0, 0],
    [0, 2, 6, 0, 0, 1, 3, 4, 5],
    [4, 7, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 2, 4, 0, 0],
    [0, 3, 0, 0, 0, 8, 0, 6, 2],
    [0, 0, 9, 7, 6, 0, 5, 0, 8]
])
solver = Sudoku(initial_board)
solver.analyze()