
ROWS = 6
COLS = 7

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    for row in board:
        print("| " + " | ".join(row) + " |")
    print("-----------------------------")
    print("  1   2   3   4   5   6   7")

print_board()


def drop_disc(column, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            return True

    return False

def undo_move(column):
    for row in range(ROWS):
        if board[row][column] != " ":
            board[row][column] = " "
            return

def check_win(player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 0

                    for i in range(4):
                        r = row + i * dr
                        c = col + i * dc

                        if (0 <= r < ROWS and
                            0 <= c < COLS and
                            board[r][c] == player):
                            count += 1
                        else:
                            break

                    if count == 4:
                        return True

    return False


def evaluate_board():
    if check_win("O"):
        return 100000
    if check_win("X"):
        return -100000

    score = 0

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for row in range(ROWS):
        for col in range(COLS):
            for dr, dc in directions:
                cells = []

                for i in range(4):
                    r = row + i * dr
                    c = col + i * dc

                    if 0 <= r < ROWS and 0 <= c < COLS:
                        cells.append(board[r][c])

                if len(cells) == 4:
                    o_count = cells.count("O")
                    x_count = cells.count("X")
                    empty = cells.count(" ")

                    if x_count == 0:
                        if o_count == 3 and empty == 1:
                            score += 50
                        elif o_count == 2 and empty == 2:
                            score += 10

                    if o_count == 0:
                        if x_count == 3 and empty == 1:
                            score -= 40
                        elif x_count == 2 and empty == 2:
                            score -= 10

    return score

def ai_move():
    best_score = -float("inf")
    best_column = None

    alpha = -float("inf")
    beta = float("inf")

    for col in range(COLS):
        if board[0][col] == " ":
            drop_disc(col, "O")

            score = minimax(3, False, alpha, beta)

            undo_move(col)

            if score > best_score:
                best_score = score
                best_column = col

            alpha = max(alpha, best_score)

    return best_column



current_player = "X"

def minimax(depth, maximizing, alpha, beta):
    score = evaluate_board()

    if abs(score) >= 100000 or depth == 0:
        return score

    if maximizing:
        best_score = -float("inf")

        for col in range(COLS):
            if board[0][col] == " ":
                drop_disc(col, "O")

                score = minimax(depth - 1, False, alpha, beta)

                undo_move(col)

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if alpha >= beta:
                    break

        return best_score

    else:
        best_score = float("inf")

        for col in range(COLS):
            if board[0][col] == " ":
                drop_disc(col, "X")

                score = minimax(depth - 1, True, alpha, beta)

                undo_move(col)

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if alpha >= beta:
                    break

        return best_score

def play_game():
    global board
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

    current_player = "X"
    while True:
        print_board()

        if current_player == "X":
            print("Your turn!")
            while True:
                try:
                    col = int(input("Enter column (1-7): ")) - 1

                    if col < 0 or col >= COLS:
                        print("Invalid column. Choose between 1 and 7.")
                    elif board[0][col] != " ":
                        print("Column is full. Choose another one.")
                    else:
                        break

                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("AI is thinking...")
            col = ai_move()
            print("AI chose column:", col + 1)

        if drop_disc(col, current_player):
            if check_win(current_player):
                print_board()
                if current_player == "X":
                    print("You win!")
                else:
                    print("AI wins!")
                break

            if all(board[0][col] != " " for col in range(COLS)):
                print_board()
                print("It's a draw!")
                break

            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"
while True:
    play_game()

    while True:
        choice = input("Do you want to play again? (yes/no): ").lower()

        if choice == "yes":
            break
        elif choice == "no":
            print("Thanks for playing!")
            exit()
        else:
            print("Invalid input. Please enter yes or no.")







