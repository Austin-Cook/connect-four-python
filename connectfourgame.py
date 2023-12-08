from connectfourboard import ConnectFourBoard, Players, GameStatus


class ConnectFourGame:
    @staticmethod
    def play():
        board = ConnectFourBoard()

        print("Welcome to Connect 4")
        print(f"One player is {Players.PLAYER_ONE.value}, and the other is {Players.PLAYER_TWO.value}\n")
        print(board)

        # take turns
        while not board.is_game_over():
            print(f"{board.turn.value}'s turn:")
            drop_col = int(input("Enter column to drop (1-7): "))
            if not board.take_turn(drop_col):
                # invalid move
                print("Invalid move, try again\n")
                continue
            print(board)

        # game over
        if board.game_status == GameStatus.DRAW:
            win_str = "It was a draw"
        else:
            winner = Players.PLAYER_ONE if board.game_status == GameStatus.PLAYER_ONE_WON \
                else Players.PLAYER_TWO
            win_str = f"Player {winner.value} won!"
        print("Game over: " + win_str)
