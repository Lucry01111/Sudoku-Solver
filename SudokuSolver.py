import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class SudokuGenerator:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.solution = np.zeros((9, 9), dtype=int)
        self.steps = []  # To store each step of the solving process

    def is_valid(self, board, row, col, num):
        """Check if the number `num` can be placed in `board[row][col]`."""
        if num in board[row]:
            return False
        if num in board[:, col]:
            return False
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        if num in board[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True

    def find_empty_location(self, board):
        """Find the first empty cell (value 0) in `board`."""
        for row in range(9):
            for col in range(9):
                if board[row, col] == 0:
                    return row, col
        return None

    def solve_sudoku_step_by_step(self, board):
        """Solve the Sudoku while recording each step."""
        empty_loc = self.find_empty_location(board)
        if not empty_loc:
            self.steps.append(board.copy())  # Puzzle solved
            return True
        
        row, col = empty_loc
        numbers = list(range(1, 10))
        random.shuffle(numbers)  # Shuffle numbers for random insertion
        
        for num in numbers:
            if self.is_valid(board, row, col, num):
                board[row, col] = num
                self.steps.append(board.copy())  # Record the current step
                if self.solve_sudoku_step_by_step(board):
                    return True
                board[row, col] = 0
                self.steps.append(board.copy())  # Record backtracking
        
        return False

    def solve_and_count_solutions(self, board, count=0):
        """Count the number of Sudoku solutions, stopping if it exceeds 1."""
        empty_loc = self.find_empty_location(board)
        if not empty_loc:
            return count + 1
        
        row, col = empty_loc
        numbers = list(range(1, 10))
        random.shuffle(numbers)  # Shuffle numbers for random insertion

        for num in numbers:
            if self.is_valid(board, row, col, num):
                board[row, col] = num
                count = self.solve_and_count_solutions(board, count)
                if count > 1:
                    return count
                board[row, col] = 0
        
        return count

    def generate_full_sudoku(self):
        """Generate a complete Sudoku grid."""
        self.solve_sudoku_step_by_step(self.board)
        self.solution = self.board.copy()

    def remove_numbers(self, num_remove):
        """Remove `num_remove` numbers from the grid, ensuring a unique solution."""
        attempts = num_remove
        while attempts > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row, col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            
            backup = self.board[row, col]
            self.board[row, col] = 0
            
            # Ensure the solution is still unique
            board_copy = self.board.copy()
            if self.solve_and_count_solutions(board_copy) != 1:
                self.board[row, col] = backup  # Restore the number
            else:
                attempts -= 1

    def generate_sudoku(self, difficulty):
        """Generate a Sudoku puzzle with the specified difficulty."""
        self.board = np.zeros((9, 9), dtype=int)
        self.generate_full_sudoku()

        num_remove = {
            'easy': 20,
            'medium': 30,
            'hard': 40,
            'extreme': 50,
        }.get(difficulty, 40)

        self.remove_numbers(num_remove)
        return self.board

    def plot_board(self, board, ax):
        ax.clear()
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 9)
        ax.set_xticks([])
        ax.set_yticks([])
        
        for i in range(10):
            lw = 2 if i % 3 == 0 else 0.5
            ax.axhline(i, color='black', linewidth=lw)
            ax.axvline(i, color='black', linewidth=lw)
        
        for row in range(9):
            for col in range(9):
                value = board[row, col]
                if value != 0:
                    ax.text(col + 0.5, 8.5 - row, str(value), ha='center', va='center', fontsize=20)
        
        ax.invert_yaxis()

def animate_solution(generator, steps):
    fig, ax = plt.subplots(figsize=(6, 6))

    def update(frame):
        ax.clear()
        generator.plot_board(steps[frame], ax)
        return ax,

    if not steps:
        print("No steps to animate. The Sudoku may not have been solved properly.")
        return
    
    ani = animation.FuncAnimation(fig, update, frames=len(steps), repeat=False, interval=500)  # Adjusted interval
    plt.show()

def main():
    while True:
        difficulty = input("Choose difficulty (easy, medium, hard, extreme): ").strip().lower()
        if difficulty in ['easy', 'medium', 'hard', 'extreme']:
            break
        print("Invalid difficulty. Please choose between 'easy', 'medium', 'hard', or 'extreme'.")

    generator = SudokuGenerator()
    sudoku_board = generator.generate_sudoku(difficulty)

    print("\nGenerated Sudoku:")
    fig, ax = plt.subplots(figsize=(6, 6))
    generator.plot_board(sudoku_board, ax)
    plt.show(block=False)  # Show the initial Sudoku board without blocking

    print("\nSolving Sudoku step-by-step...")
    generator.steps.clear()  # Clear steps before solving
    generator.solve_sudoku_step_by_step(sudoku_board)  # Re-run solving
    animate_solution(generator, generator.steps)

if __name__ == "__main__":
    main()