import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, root):  # Fixed the constructor name
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("400x450")

        # Create a 9x9 grid
        self.board = [[0] * 9 for _ in range(9)]
        self.entries = [[None] * 9 for _ in range(9)]

        # Generate a Sudoku puzzle
        self.generate_puzzle()

        # Draw the board
        self.draw_board()

        # Add solve button
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.pack(pady=10)

    def draw_board(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for row in range(9):
            for col in range(9):
                entry = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                entry.grid(row=row, column=col, padx=5, pady=5)

                # Pre-fill entries from the board
                if self.board[row][col] != 0:
                    entry.insert(0, str(self.board[row][col]))
                    entry.config(state="disabled", disabledforeground="black")

                self.entries[row][col] = entry

    def generate_puzzle(self):
        """Generates a random Sudoku puzzle using backtracking."""
        self.fill_grid(self.board)
        self.remove_numbers(self.board)

    def fill_grid(self, grid):
        """Fills the grid with a complete valid Sudoku solution."""
        numbers = list(range(1, 10))
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self.fill_grid(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    def remove_numbers(self, grid):
        """Removes numbers from the grid to create a puzzle."""
        for _ in range(30):  # Remove 30 numbers
            row, col = random.randint(0, 8), random.randint(0, 8)
            while grid[row][col] == 0:  # Avoid removing the same number twice
                row, col = random.randint(0, 8), random.randint(0, 8)
            grid[row][col] = 0

    def is_valid(self, grid, row, col, num):
        """Checks if a number can be placed in a cell."""
        # Check row and column
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False

        return True

    def solve_sudoku(self):
        """Solves the Sudoku using backtracking."""
        def backtrack_solve():
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        for num in range(1, 10):
                            if self.is_valid(self.board, row, col, num):
                                self.board[row][col] = num
                                if backtrack_solve():
                                    return True
                                self.board[row][col] = 0
                        return False
            return True

        # Update the board based on user inputs
        for row in range(9):
            for col in range(9):
                value = self.entries[row][col].get()
                self.board[row][col] = int(value) if value.isdigit() else 0

        if backtrack_solve():
            # Update the UI with the solution
            for row in range(9):
                for col in range(9):
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(self.board[row][col]))
        else:
            messagebox.showerror("Error", "No solution exists for the given Sudoku puzzle.")

if __name__ == "__main__":  # Fixed the special variable check
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
