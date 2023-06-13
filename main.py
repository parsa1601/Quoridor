from MiniMaxPlayer import MiniMaxPlayer
from Board import Board



if __name__ == "__main__":
    board = Board()

    white_player = MiniMaxPlayer("white", 4 , 8 , board)
    black_player = MiniMaxPlayer("black", 4 , 0 , board)

    walls_count = 0


    while True:
        action = white_player.minimax_decider(opponent =  black_player)

        white_player.play(action)
        board.print_map()
        print(
            f"white: {action}, left walls: {white_player.walls_count}"
        )

        if white_player.is_winner():
            print(f"White player just won with {white_player.moves_count} moves!")
            break
        if action.split("#")[0] == "wall":
            walls_count += 1

        action = black_player.minimax_decider(opponent=white_player)

        black_player.play(action)

        board.print_map()

        print(
            f"black: {action}, left walls: {black_player.walls_count}"
        )

        if black_player.is_winner():
            print(f"Black player just won with {black_player.moves_count} moves!")
            break

        if action.split("#")[0] == "wall":
            walls_count += 1

    print(f"walls count {walls_count}")

