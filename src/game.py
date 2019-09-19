from src.player import Player
from src.board import Board


class Game:

    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None

    def main(self):
        """ Initialize board size and players """
        print("Tic-Tac-Toe\n")
        size = 0
        while size == 0:
            size = input("What size board would you like to play on? (min 3, max 10) (ie. 3 for 3x3) ")
            if not size.isdigit() or int(size) not in range(3, 11):
                size = 0
                print("Enter valid whole number.\n")

        self.board = Board(size)

        player1_name = input("Player 1 Name: ")
        player2_name = input("Player 2 Name: ")
        self.player1 = Player(player1_name, "X")
        self.player2 = Player(player2_name, "O")

        self.start_game()

    def start_game(self):
        """
        Calls player turns and checks after every turn if player has won
        Reports winner and calls function 'reset_game' after

        :return: None
        """
        self.board.init_positions()

        num_turns = 0
        winner = False
        current_player = self.player1
        while not winner:
            num_turns += 1
            location, keys = self.turn(current_player)
            winner = self.board.check_is_winning_board(location, keys)
            if winner:
                print("Player: {} WON!".format(current_player.name))
                current_player.add_win()
            # tie game if turns = spaces in board
            if num_turns == (self.board.size * self.board.size):
                print("No winners. Tie Game.")
                break
            # switch current player
            current_player = self.player2 if current_player == self.player1 else self.player1

        self.reset_game()

    def turn(self, player):
        """
        Prompts player for a position key, if valid, adds the position to the board

        :param player: Player who's turn it is
        :return: location of player's turn
        """
        print(self.board.generate_board())
        print("{}'s Turn".format(player.name))
        position_key = None
        while not self.validate_position_key(position_key):
            self.prompt_options()
            position_key = input("Enter position key: ")
        # convert position key string to int list
        position_key = [int(k) for k in position_key]
        location = self.add_position(position_key, player.token)
        return location, position_key

    def prompt_options(self):
        """
        Prompts player with a list of valid option commands
        exit : end's game
        help : shows position key map
        Y : continue with game

        :return: bool if invalid input false, else true
        """
        user_input = ""
        while user_input.upper() != "Y":
            user_input = input("To print board position to key map. Enter 'help'. "
                               "To continue, enter 'Y'. "
                               "To exit, enter 'exit' ")
            if user_input == "help":
                print(self.board.generate_board(help=True))
            elif user_input == "exit":
                self.reset_game()
            elif user_input.upper() != "Y":
                print("Invalid input")
        return True

    def validate_position_key(self, key):
        """
        Ensures that the entered position key is a valid entry

        :param key: position key to check
        :return: bool, if position key is valid or not
        """
        if not key:
            return False
        if not key.isdigit():
            print("Invalid position key. Enter digits.\n")
            return False
        if len(key) != 2:
            print("Invalid position key. Enter 2 digits.\n")
            return False
        str_keys = list(key)
        keys = [int(k) for k in str_keys]
        for k in keys:
            # if key in key pair is less than 0 or greater/equal to board size or that position
            # on the board isn't empty
            if k < 0 or k >= self.board.size:
                print("Invalid position key. Out of range.\n")
                return False
            if self.board.positions[keys[0]][keys[1]] != "_":
                print("Invalid position key. Position already taken.\n")
                return False
        return True

    def add_position(self, keys, token):
        """
        Updates the current positions on the grid and
        returns where that position is on the grid

        :param keys: position key to set
        :param token: player's token to set
        :return: the location of the position key
                 one of ["EDGE", "CORNER", "DIAGONAL", "OTHER"]
        """
        max_position = self.board.size - 1
        self.board.positions[keys[0]][keys[1]] = token

        if keys[0] in [0, max_position] and keys[1] in [0, max_position]:
            return "CORNER"
        if 0 in keys or max_position in keys:
            return "EDGE"
        if self._is_diagonal_position(keys):
            return "DIAGONAL"
        return "OTHER"

    def _is_diagonal_position(self, keys):
        """ Checks if requested position key is on a diagonal """
        if keys[0] == keys[1]:
            return True
        for i in range(0, self.board.size):
            if keys[1] == i and keys[0] == (self.board.size - 1 - i):
                return True
        return False

    def reset_game(self):
        """
        Resets game if user requests, else end of program

        :return: None
        """
        print(self.board.generate_board())
        print("Game Over")
        repeat = input("Play again? Y or any key to exit: ")
        if repeat.upper() == "Y":
            self.show_scoreboard()
            self.player1.change_token()
            self.player2.change_token()
            self.start_game()
        else:
            print("Thanks for playing!")
            # exits application
            exit()

    def show_scoreboard(self):
        """ Prints names and scores of players """
        print("\nScoreboard:")
        print("{}: {}".format(self.player1.name, self.player1.wins))
        print("{}: {}".format(self.player2.name, self.player2.wins))


if __name__ == "__main__":
    game = Game()
    game.main()
