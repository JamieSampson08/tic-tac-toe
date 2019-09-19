class Board:
    def __init__(self, size):
        self.size = int(size)
        self.positions = []

    def generate_board(self, help=False):
        """
        Generates the board based on piece positions or position keys
        Can't both show positions and the help grid

        :param help: show positions keys
        :return: string, grid
        """
        grid = ""
        for row in range(0, self.size):
            if self.positions:
                col = [self.positions[row][i] for i in range(0, self.size)]
            if help:
                col = [str(row) + str(i) for i in range(0, self.size)]
            grid += " | ".join(col) + "\n"
        return grid

    def init_positions(self):
        """ Fills all positions with underscores (empty) """
        self.positions = []
        for row in range(0, self.size):
            self.positions.append([])
            for col in range(0, self.size):
                self.positions[row].append("_")

    def check_is_winning_board(self, location, keys):
        """
        Checks to see if positions on board results in a winner

        :param: keys: location of new placement
        :param location: location of player's turn one of
            CORNER: all four corners of board
            EDGE: all spaces along edge of board (not including corners)
            DIAGONAL: space along left/right or right/left diagonals
            OTHER: all other spaces that don't fall in any of the above categories
        :return: token of winner if winning board, else None
        """

        token = self.positions[keys[0]][keys[1]]
        # only check vertical and horizontal, diagonal isn't possible
        if location in ["EDGE", "OTHER"]:
            return (
                    self.check_horizontal(keys, token) or
                    self.check_vertical(keys, token)
            )
        # check vertical, horizontal, diagonals (left/right & right/left)
        return (
                self.check_horizontal(keys, token) or
                self.check_vertical(keys, token) or
                self.check_right_left_diagonal(token) or
                self.check_left_right_diagonal(token)
        )

    """
    Following functions check 4 types of winning configurations
    """

    def check_vertical(self, keys, token):
        """ top to bottom """
        for i in range(0, self.size):
            if self.positions[i][keys[1]] != token:
                return False
        return True

    def check_horizontal(self, keys, token):
        """ left to right """
        for i in range(0, self.size):
            if self.positions[keys[0]][i] != token:
                return False
        return True

    def check_right_left_diagonal(self, token):
        """ top right to bottom left """
        for i in range(0, self.size):
            if self.positions[self.size - 1 - i][i] != token:
                return False
        return True

    def check_left_right_diagonal(self, token):
        """ top left to bottom right """
        for i in range(0, self.size):
            if self.positions[i][i] != token:
                return False
        return True
