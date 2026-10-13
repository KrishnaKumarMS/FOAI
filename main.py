"""
Multi-Game AI Application
---------------------------
A single entry point offering three classic AI search/CSP demos:

  1. Tic-Tac-Toe  -> Minimax + Alpha-Beta Pruning (adversarial search)
  2. Maze Solver  -> A* Search (informed/heuristic search)
  3. Sudoku       -> CSP + Backtracking (constraint satisfaction)

Run:  python main.py
"""

import tictactoe
import maze_solver
import sudoku_solver


def menu():
    while True:
        print("\n" + "=" * 40)
        print(" MULTI-GAME AI APPLICATION")
        print("=" * 40)
        print("1. Tic-Tac-Toe   (Minimax + Alpha-Beta)")
        print("2. Maze Solver   (A* Search)")
        print("3. Sudoku        (CSP + Backtracking)")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            tictactoe.play()
        elif choice == "2":
            maze_solver.solve()
        elif choice == "3":
            sudoku_solver.run()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-4.")


if __name__ == "__main__":
    menu()
