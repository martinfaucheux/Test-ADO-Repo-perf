# tic tac toe game

board = [[" " for i in range(3)] for j in range(3)]


def draw_board():
    print("  0 1 2")
    for i in range(3):
        print(f"{i} {board[i][0]}|{board[i][1]}|{board[i][2]}")
        if i < 2:
            print("  -----")


def get_move(player):
    while True:
        move = input(f"{player}, enter your move (row column): ")
        try:
            row, col = map(int, move.split())
            if row in [0, 1, 2] and col in [0, 1, 2] and board[row][col] == " ":
                return (row, col)
            else:
                print("Invalid move, try again.")
        except ValueError:
            print("Invalid input, try again.")


def make_move(player, row, col):
    board[row][col] = player


def has_won(player):
    # check rows
    for row in range(3):
        if (
            board[row][0] == player
            and board[row][1] == player
            and board[row][2] == player
        ):
            return True
    # check columns
    for col in range(3):
        if (
            board[0][col] == player
            and board[1][col] == player
            and board[2][col] == player
        ):
            return True
    # check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False


def main():
    draw_board()
    while True:
        row, col = get_move("X")
        make_move("X", row, col)
        draw_board()
        if has_won("X"):
            print("X has won!")
            break
        row, col = get_move("O")
        make_move("O", row, col)
        draw_board()
        if has_won("O"):
            print("O has won!")
            break


main()
