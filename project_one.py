"""
Name: Bola Olowosago
Project: Konane
"""

import random


def generate_board(n):
    """
    Generates an n x n Konane board with alternating 1 and 2.
    Returns empty list if n <= 0.
    """
    if n <= 0:
        return []

    board = []
    for r in range(n):
        row = []
        for c in range(n):
            if (r + c) % 2 == 0:
                row.append(1)
            else:
                row.append(2)
        board.append(row)

    return board


def get_board_as_string(board):
    """
    Returns the board formatted correctly.
    """
    if not board:
        return ""

    rows = len(board)
    cols = len(board[0])

    result = "   "
    for c in range(cols):
        result += str(c % 10) + " "
    result = result.rstrip() + "\n"

    for r in range(rows):
        result += "  +" + "-+" * cols + "\n"
        result += str(r % 10) + " |"

        for c in range(cols):
            if board[r][c] == 0:
                result += " |"
            elif board[r][c] == 1:
                result += "●|"
            else:
                result += "○|"

        result += "\n"

    result += "  +" + "-+" * cols + "\n"

    return result


def prep_board_human(board):
    """
    Prompts user to remove two valid starting tokens.
    Both tokens must:
    - Not be on the edge
    - Be different colors
    """
    rows = len(board)
    cols = len(board[0])

    print(get_board_as_string(board))

    # First token
    while True:
        r1 = int(input())
        c1 = int(input())

        if not (0 <= r1 < rows and 0 <= c1 < cols):
            continue
        if board[r1][c1] == 0:
            continue
        if r1 == 0 or r1 == rows - 1 or c1 == 0 or c1 == cols - 1:
            continue
        break

    # Second token
    while True:
        r2 = int(input())
        c2 = int(input())

        if not (0 <= r2 < rows and 0 <= c2 < cols):
            continue
        if board[r2][c2] == 0:
            continue
        if r2 == 0 or r2 == rows - 1 or c2 == 0 or c2 == cols - 1:
            continue
        if (r1, c1) == (r2, c2):
            continue
        if board[r1][c1] == board[r2][c2]:
            continue
        break

    board[r1][c1] = 0
    board[r2][c2] = 0


def is_valid_move(board, move):
    """
    Returns True if the move follows Konane rules.
    """
    if not board:
        return False

    rows = len(board)
    cols = len(board[0])

    (r1, c1), (r2, c2) = move

    if not (0 <= r1 < rows and 0 <= c1 < cols):
        return False
    if not (0 <= r2 < rows and 0 <= c2 < cols):
        return False

    player = board[r1][c1]
    if player == 0:
        return False

    if board[r2][c2] != 0:
        return False

    if r1 != r2 and c1 != c2:
        return False

    opponent = 2 if player == 1 else 1

    if r1 == r2:
        distance = abs(c2 - c1)
        if distance < 2 or distance % 2 != 0:
            return False

        step = 1 if c2 > c1 else -1
        col = c1 + step
        count = 0

        while col != c2:
            if count % 2 == 0:
                if board[r1][col] != opponent:
                    return False
            else:
                if board[r1][col] != 0:
                    return False
            col += step
            count += 1

    else:
        distance = abs(r2 - r1)
        if distance < 2 or distance % 2 != 0:
            return False

        step = 1 if r2 > r1 else -1
        row = r1 + step
        count = 0

        while row != r2:
            if count % 2 == 0:
                if board[row][c1] != opponent:
                    return False
            else:
                if board[row][c1] != 0:
                    return False
            row += step
            count += 1

    return True


def get_valid_moves_for_stone(board, stone):
    """
    Returns a list of all valid moves for a given stone.
    If the stone location is empty or invalid, returns an empty list.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = stone

    if not (0 <= r < rows and 0 <= c < cols):
        return []

    if board[r][c] == 0:
        return []

    moves = []
    for r2 in range(rows):
        for c2 in range(cols):
            move = ((r, c), (r2, c2))
            if is_valid_move(board, move):
                moves.append(move)

    return moves


def get_valid_moves(board, player):
    """
    Returns all valid moves for a given player.
    """
    rows = len(board)
    cols = len(board[0])

    all_moves = []

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == player:
                stone_moves = get_valid_moves_for_stone(board, (r, c))
                for m in stone_moves:
                    all_moves.append(m)

    return all_moves


def human_player(board, player):
    """
    Prompts the user for a valid move and returns it.
    Returns empty tuple if no valid moves.
    """
    valid_moves = get_valid_moves(board, player)

    if not valid_moves:
        return ()

    valid = False
    while not valid:
        print(get_board_as_string(board))

        r1 = int(input())
        c1 = int(input())
        r2 = int(input())
        c2 = int(input())

        move = ((r1, c1), (r2, c2))

        if is_valid_move(board, move):
            valid = True

    return move


def random_player(board, player):
    """
    Returns a random valid move.
    """
    moves = get_valid_moves(board, player)
    if not moves:
        return ()
    return random.choice(moves)


def ai_player(board, player):
    """
    Chooses the move that captures the most pieces.
    """
    moves = get_valid_moves(board, player)

    if not moves:
        return ()

    best_move = moves[0]
    best_score = 0

    for move in moves:
        (r1, c1), (r2, c2) = move

        if r1 == r2:
            score = abs(c2 - c1) // 2
        else:
            score = abs(r2 - r1) // 2

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def apply_move(board, move):
    """
    Updates the board after a move.
    """
    (r1, c1), (r2, c2) = move
    player = board[r1][c1]
    board[r1][c1] = 0

    if r1 == r2:
        step = 1 if c2 > c1 else -1
        col = c1 + step
        count = 0
        while col != c2:
            if count % 2 == 0:
                board[r1][col] = 0
            col += step
            count += 1
    else:
        step = 1 if r2 > r1 else -1
        row = r1 + step
        count = 0
        while row != r2:
            if count % 2 == 0:
                board[row][c1] = 0
            row += step
            count += 1

    board[r2][c2] = player


def play_game(board):
    """
    Plays a full AI vs AI game and returns the winner.
    """
    current_player = random.choice([1, 2])

    while True:
        move = ai_player(board, current_player)

        if move == ():
            return 2 if current_player == 1 else 1

        apply_move(board, move)
        current_player = 2 if current_player == 1 else 1