class Player:
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.wins = 0

    def change_token(self):
        """ Changes a player's token for the board """
        token = ""
        change = True
        message = "\n(Optional) Change {} playing token? (single characters only, `|` or `_` not allowed) "
        while len(token) != 1:
            token = input(message.format(self.name))
            if len(token) == 0:
                change = False
                break
            if token == '|' or token == '_':
                print("Invalid token. '|' or '_' not allowed.")
                token = ""
        if change:
            self.token = token

    def add_win(self):
        """ Increments a player's win score by 1 """
        self.wins += 1
