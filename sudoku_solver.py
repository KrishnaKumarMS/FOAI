"""
Sudoku Solver with CSP + Backtracking
---------------------------------------
Model: Constraint Satisfaction Problem (CSP).
- Variables : each empty cell.
- Domain    : digits 1-9.
- Constraints: no repeated digit in any row, column, or 3x3 box.
- Backtracking search assigns a value, checks constraints, and backtracks
  when a dead end is reached.
- Minor optimization included: pick the empty cell with the fewest legal
  candidates first (a simple form of the "Minimum Remaining Values" CSP
  heuristic), which reduces branching a lot vs. plain left-to-right scan.
"""

EMPTY = 0

DEFAULT_PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def print_grid(grid):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-" * 21)
        row_str = ""
        for c in range(9):
            if c % 3 == 0 and c != 0:
                row_str += "| "
            row_str += (str(grid[r][c]) if grid[r][c] != EMPTY else ".") + " "
        print(row_str)


def is_valid(grid, row, col, num):
    # Row constraint
    if num in grid[row]:
        return False
    # Column constraint
    if num in [grid[r][col] for r in range(9)]:
        return False
    # 3x3 box constraint
    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if grid[r][c] == num:
                return False
    return True


def find_best_empty_cell(grid):
    """
    CSP heuristic: choose the empty cell with the fewest possible
    candidate values (Minimum Remaining Values). Speeds up backtracking
    a lot compared to always picking the first empty cell.
    Returns (row, col, candidates) or None if the grid is full.
    """
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == EMPTY:
                candidates = [n for n in range(1, 10) if is_valid(grid, r, c, n)]
                if best is None or len(candidates) < len(best[2]):
                    best = (r, c, candidates)
                    if len(candidates) == 1:
                        return best  # can't do better than 1 option
    return best


def solve(grid):
    """Backtracking search over the CSP. Mutates grid in place. Returns True/False."""
    cell = find_best_empty_cell(grid)
    if cell is None:
        return True  # no empty cells left -> solved

    row, col, candidates = cell
    if not candidates:
        return False  # dead end, trigger backtrack

    for num in candidates:
        grid[row][col] = num
        if solve(grid):
            return True
        grid[row][col] = EMPTY  # backtrack

    return False


def run(puzzle=None):
    grid = [row[:] for row in (puzzle or DEFAULT_PUZZLE)]
    print("Puzzle:")
    print_grid(grid)

    if solve(grid):
        print("\nSolved:")
        print_grid(grid)
    else:
        print("\nNo solution exists for this puzzle.")


if __name__ == "__main__":
    run()
