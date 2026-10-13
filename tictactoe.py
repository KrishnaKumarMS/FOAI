"""
Tic-Tac-Toe with Minimax + Alpha-Beta Pruning
----------------------------------------------
Model: Adversarial search.
- The board is the "state".
- Minimax explores all future states assuming both players play optimally.
- Alpha-Beta pruning cuts off branches that can't affect the final decision,
  making the search faster without changing the result.

Human = 'X', AI = 'O'. AI never loses.
"""

HUMAN = 'X'
AI = 'O'
EMPTY = ' '


def print_board(board):
    print()
    for r in range(3):
        row = board[r * 3: r * 3 + 3]
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if r < 2:
            print("---+---+---")
    print()


def winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    for a, b, c in lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def game_over(board):
    return winner(board) is not None or is_full(board)


def score(board, depth):
    w = winner(board)
    if w == AI:
        return 10 - depth      # prefer faster wins
    elif w == HUMAN:
        return depth - 10      # prefer slower losses
    return 0


def minimax(board, depth, alpha, beta, is_maximizing):
    """
    Core AI model.
    is_maximizing = True  -> AI's turn (wants highest score)
    is_maximizing = False -> Human's turn (wants lowest score)
    alpha = best value maximizer can guarantee so far
    beta  = best value minimizer can guarantee so far
    """
    if game_over(board):
        return score(board, depth)

    if is_maximizing:
        best = float('-inf')
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                val = minimax(board, depth + 1, alpha, beta, False)
                board[i] = EMPTY
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # prune: minimizer will never let this happen
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                val = minimax(board, depth + 1, alpha, beta, True)
                board[i] = EMPTY
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break  # prune: maximizer will never let this happen
        return best


def best_move(board):
    best_val = float('-inf')
    move = None
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            val = minimax(board, 0, float('-inf'), float('inf'), False)
            board[i] = EMPTY
            if val > best_val:
                best_val = val
                move = i
    return move


def play():
    board = [EMPTY] * 9
    print("Tic-Tac-Toe: You are 'X', AI is 'O'.")
    print("Positions are numbered 1-9 like a phone keypad layout:")
    print(" 1 | 2 | 3 \n 4 | 5 | 6 \n 7 | 8 | 9 ")
    print_board(board)

    current = HUMAN
    while not game_over(board):
        if current == HUMAN:
            move = None
            while move is None:
                try:
                    raw = int(input("Your move (1-9): ")) - 1
                    if 0 <= raw <= 8 and board[raw] == EMPTY:
                        move = raw
                    else:
                        print("Invalid move, try again.")
                except ValueError:
                    print("Enter a number 1-9.")
            board[move] = HUMAN
        else:
            print("AI is thinking...")
            move = best_move(board)
            board[move] = AI
            print(f"AI plays position {move + 1}")

        print_board(board)
        current = AI if current == HUMAN else HUMAN

    w = winner(board)
    if w == HUMAN:
        print("You win! (this shouldn't normally happen against optimal AI)")
    elif w == AI:
        print("AI wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    play()
