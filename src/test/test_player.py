from mock import patch
from src.player import Player
from src.test.utils import BaseTestCase, captured_output


class TestPlayerBase(BaseTestCase):
    def setUp(self):
        super(TestPlayerBase, self).setUp()
        self.player = Player("Jamie", "O")

    def test_base_case(self):
        self.assertEqual(self.player.name, "Jamie")
        self.assertEqual(self.player.token, "O")
        self.assertEqual(self.player.wins, 0)

    def test_add_win(self):
        self.player.add_win()
        self.assertEqual(self.player.wins, 1)


class TestChangePlayerToken(BaseTestCase):
    def test_base_case(self):
        user_input = ['&']

        with patch('builtins.input', side_effect=user_input):
            self.game.player1.change_token()

        self.assertEqual(self.game.player1.token, "&")

    def test_invalid_token(self):
        user_input = ["|", '_', '*']
        exp = ["Invalid token. '|' or '_' not allowed.",
               "Invalid token. '|' or '_' not allowed."]

        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                self.game.player1.change_token()

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))

        self.assertEqual(self.game.player1.token, "*")
