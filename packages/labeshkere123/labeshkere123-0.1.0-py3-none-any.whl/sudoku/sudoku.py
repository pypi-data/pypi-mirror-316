class Sudoku:
    def __init__(self, board):
        self.board = board

    def is_valid(self, row, col, num):
        # Проверка строки
        if num in self.board[row]:
            return False

        # Проверка столбца
        for r in range(9):
            if self.board[r][col] == num:
                return False

        # Проверка 3x3 квадрата
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False

        return True

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def solve(self):
        empty_cell = self.find_empty()
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0  # Возврат назад

        return False

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))

    def analyze(self):
        non_zero_count = sum(1 for row in self.board for num in row if num != 0)
        if non_zero_count < 17:
            print("Мало чисел для решения судоку")
            return

        if self.solve():
            print("Судоку решено:)")
            self.print_board()
        else:
            print("Судоку невозможно решать:(")


initial_board = [
    [5, 0, 0, 4, 0, 7, 9, 0, 3],
    [0, 0, 2, 0, 1, 0, 0, 8, 7],
    [1, 0, 0, 6, 8, 0, 0, 0, 4],
    [8, 0, 0, 3, 0, 0, 7, 0, 0],
    [0, 2, 6, 0, 0, 1, 3, 4, 5],
    [4, 7, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 2, 4, 0, 0],
    [0, 3, 0, 0, 0, 8, 0, 6, 2],
    [0, 0, 9, 7, 6, 0, 5, 0, 8]
]

solver = Sudoku(initial_board)
solver.analyze()
