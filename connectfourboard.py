from enum import Enum, auto


class Players(Enum):
    EMPTY = '-'
    PLAYER_ONE = 'X'
    PLAYER_TWO = 'O'


class GameStatus(Enum):
    PLAYER_ONE_WON = auto()
    PLAYER_TWO_WON = auto()
    NOT_OVER = auto()
    DRAW = auto()


class ConnectFourBoard:
    def __init__(self):
        # Use 6 x 7 grid
        self.board = [[Players.EMPTY] * 7 for _ in range(6)]
        self.turn = Players.PLAYER_ONE
        self.game_status = GameStatus.NOT_OVER

    def take_turn(self, drop_col: int) -> bool:
        """
        The current player takes their turn

        :param drop_col: The column where the player desired to drop a piece, as an int 1-7
        :return: False if the column is already full, True otherwise
        """
        assert 1 <= drop_col <= 7, f"Invalid column ({drop_col}), must be 1-7"

        # 0 based indexing
        drop_col -= 1

        if self.board[0][drop_col] is not Players.EMPTY:
            # column already full
            return False

        # place the piece
        for row in range(5, -1, -1):
            if self.board[row][drop_col] == Players.EMPTY:
                # place here
                self.board[row][drop_col] = self.turn
                break

        # next player's turn
        self.turn = Players.PLAYER_ONE if self.turn == Players.PLAYER_TWO else Players.PLAYER_TWO

        return True

    def is_game_over(self) -> bool:
        """
        Checks if the game is over and sets self.game_status

        :return: True if the game is over, False otherwise
        """
        # check if a player has 4 in a row
        if self._player_won(Players.PLAYER_ONE):
            self.game_status = GameStatus.PLAYER_ONE_WON
            return True
        if self._player_won(Players.PLAYER_TWO):
            self.game_status = GameStatus.PLAYER_TWO_WON
            return True

        # check for draw (board is full)
        self.game_status = GameStatus.DRAW
        for top_slot in self.board[0]:
            if top_slot == Players.EMPTY:
                # at least one more empty space
                self.game_status = GameStatus.NOT_OVER

        # game over if there was a draw
        return True if self.game_status == GameStatus.DRAW else False

    def _player_won(self, player: Players) -> bool:
        """
        Checks if player has four pieces in a row\n
        Method: For each direction to check, start at each valid starting place,
        and check 4 spaces moving in the curr direction

        :param player: The player to check for
        :return: The result, as a boolean
        """
        # row       col       down-right down-left
        # |xxxx---| |xxxxxxx| |xxxx---| |---xxxx|
        # |xxxx---| |xxxxxxx| |xxxx---| |---xxxx|
        # |xxxx---| |xxxxxxx| |xxxx---| |---xxxx|
        # |xxxx---| |-------| |-------| |-------|
        # |xxxx---| |-------| |-------| |-------|
        # |xxxx---| |-------| |-------| |-------|

        # rows
        for row in range(6):
            for col in range(4):
                valid = True
                for offset in range(4):
                    if self.board[row][col + offset] != player:
                        # not four in row starting at curr [row][col]
                        valid = False
                        break
                if valid:
                    return True

        # cols
        for row in range(3):
            for col in range(7):
                valid = True
                for offset in range(4):
                    if self.board[row + offset][col] != player:
                        # not four in col starting at curr [row][col]
                        valid = False
                        break
                if valid:
                    return True

        # diagonal down-right
        for row in range(3):
            for col in range(4):
                valid = True
                for offset in range(4):
                    if self.board[row + offset][col + offset] != player:
                        # not four in diagonal starting at curr [row][col]
                        valid = False
                        break
                if valid:
                    return True

        # diagonal down-left
        for row in range(3):
            for col in range(3, 7):
                valid = True
                for offset in range(4):
                    if self.board[row - offset][col - offset] != player:
                        # not four in diagonal starting at curr [row][col]
                        valid = False
                        break
                if valid:
                    return True

        # no valid path found
        return False

    def __str__(self):
        string = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        for row in self.board:
            for col in row:
                string += "| " + str(col.value) + ' '
            string += '|\n'
        string += "|---------------------------|\n"
        string += "| 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n"
        string += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

        return string
