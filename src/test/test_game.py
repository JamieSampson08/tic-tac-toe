from mock import patch

from src.board import Board
from src.game import Game
from src.player import Player
from src.test.utils import BaseTestCase, captured_output


class TestMain(BaseTestCase):
    def setUp(self):
        super(TestMain, self).setUp()
        self.start_game = patch.object(Game, "start_game").start()
        self.game.player1 = None
        self.game.player2 = None

    def test_base_case(self):
        user_input = ["3", 'Thor', 'Spiderman']
        exp = ["Tic-Tac-Toe"]

        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                self.game.main()

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))

        self.assertEqual(self.game.board.size, 3)
        self.assertEqual(self.game.player1.name, "Thor")
        self.assertEqual(self.game.player2.name, "Spiderman")
        self.assertEqual(self.game.player1.token, "X")
        self.assertEqual(self.game.player2.token, "O")
        self.assertTrue(self.start_game.called)

    def test_valid_size_min(self):
        user_input = ["1", "4", 'Thor', 'Spiderman']
        exp = ["Tic-Tac-Toe", "Enter valid whole number."]

        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                self.game.main()

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))

        self.assertTrue(self.start_game.called)

    def test_valid_size_max(self):
        user_input = ["20", "4", 'Thor', 'Spiderman']
        exp = ["Tic-Tac-Toe", "Enter valid whole number."]

        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                self.game.main()

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))

        self.assertTrue(self.start_game.called)


class TestStartGame(BaseTestCase):
    def setUp(self):
        super(TestStartGame, self).setUp()

        self.init_positions = patch.object(Board, "init_positions").start()
        self.init_positions.return_vale = [
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"]
        ]
        self.turn = patch.object(Game, "turn").start()
        self.turn.return_value = "Corner", [0, 0]
        self.check_winning_board = patch.object(Board, "check_is_winning_board").start()

        self.p1_add_win = patch.object(self.game.player1, "add_win").start()
        self.p2_add_win = patch.object(self.game.player2, "add_win").start()
        self.reset_game = patch.object(Game, "reset_game").start()

    def test_base_case(self):
        exp = ["Player: Toothless WON!"]
        self.check_winning_board.return_value = True

        with captured_output() as out:
            self.game.start_game()

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))

        self.assertTrue(self.p1_add_win.called)
        self.assertFalse(self.p2_add_win.called)
        self.assertTrue(self.reset_game.called)

    def test_tie_game(self):
        exp = ["No winners. Tie Game."]
        self.check_winning_board.return_value = False

        with captured_output() as out:
            self.game.start_game()

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))

        self.assertEqual(self.turn.call_count, 9)
        self.assertEqual(self.check_winning_board.call_count, 9)
        self.assertTrue(self.reset_game.called)


class TestTurn(BaseTestCase):
    def setUp(self):
        super(TestTurn, self).setUp()
        self.player = Player("Thor", "X")

        self.generate_board = patch.object(Board, "generate_board").start()
        self.generate_board.return_value = ""
        self.prompt_options = patch.object(Game, "prompt_options").start()
        self.validate_position_key = patch.object(Game, "validate_position_key").start()
        self.validate_position_key.side_effect = [False, True]

        self.add_position = patch.object(Game, "add_position").start()
        self.add_position.return_value = "CORNER"

    def test_base_case(self):
        user_input = ["00"]
        exp = ["Thor's Turn"]

        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                location, position_key = self.game.turn(self.player)

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))

        self.assertTrue(self.generate_board.called)
        self.assertEqual(self.prompt_options.call_count, 1)
        self.assertEqual(self.validate_position_key.call_count, 2)
        self.add_position.called_with([0, 0], "X")
        self.assertEqual(location, "CORNER")
        self.assertEqual(position_key, [0, 0])


class TestPromptHelpBoard(BaseTestCase):
    def setUp(self):
        super(TestPromptHelpBoard, self).setUp()
        self.generate_board = patch.object(Board, "generate_board").start()

    def test_base_case(self):
        user_input = ["Y"]

        with patch('builtins.input', side_effect=user_input):
            resp = self.game.prompt_options()

        self.assertTrue(resp)

    def test_invalid_input(self):
        user_input = ["N", "Y"]
        exp = ["Invalid input"]

        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                resp = self.game.prompt_options()

        out = out.getvalue().split("\n")
        self.assertTrue(all(msg in out for msg in exp))
        self.assertTrue(resp)

    def test_help(self):
        user_input = ["help", "Y"]

        with patch('builtins.input', side_effect=user_input):
            resp = self.game.prompt_options()

        self.assertTrue(resp)
        self.generate_board.assert_called_with(help=True)


class TestValidatePositionKey(BaseTestCase):
    def setUp(self):
        super(TestValidatePositionKey, self).setUp()
        self.game.board.positions = [
            ["O", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"]
        ]

    def test_base_case(self):
        resp = self.game.validate_position_key("01")
        self.assertTrue(resp)

    def test_no_key(self):
        resp = self.game.validate_position_key(None)
        self.assertFalse(resp)

    def test_key_not_digit(self):
        with captured_output() as out:
            resp = self.game.validate_position_key("a")

        out = out.getvalue()
        self.assertFalse(resp)
        self.assertEqual(out, "Invalid position key. Enter digits.\n\n")

    def test_key_too_long(self):
        with captured_output() as out:
            resp = self.game.validate_position_key("123")
        out = out.getvalue()
        self.assertFalse(resp)
        self.assertEqual(out, "Invalid position key. Enter 2 digits.\n\n")

    def test_key_too_short(self):
        with captured_output() as out:
            resp = self.game.validate_position_key("1")
        out = out.getvalue()
        self.assertFalse(resp)
        self.assertEqual(out, "Invalid position key. Enter 2 digits.\n\n")


    def test_invalid_out_of_range(self):
        with captured_output() as out:
            resp = self.game.validate_position_key("99")
        out = out.getvalue()
        self.assertFalse(resp)
        self.assertEqual(out, "Invalid position key. Out of range.\n\n")

    def test_invalid_position_taken(self):
        with captured_output() as out:
            resp = self.game.validate_position_key("00")
        out = out.getvalue()
        self.assertFalse(resp)
        self.assertEqual(out, "Invalid position key. Position already taken.\n\n")


class TestAddPosition(BaseTestCase):
    def setUp(self):
        super(TestAddPosition, self).setUp()
        self.game.board = Board(5)
        self.token = "X"
        self.game.board.positions = [
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]

    def test_base_case(self):
        key = [2, 1]
        exp = [
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "X", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]
        location = self.game.add_position(key, self.token)
        self.assertEqual(location, "OTHER")
        self.assertEqual(self.game.board.positions, exp)

    def test_corner_top_right(self):
        key = [0, 0]
        exp = [
            ["X", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]
        location = self.game.add_position(key, self.token)
        self.assertEqual(location, "CORNER")
        self.assertEqual(self.game.board.positions, exp)

    def test_corner_bottom_left(self):
        key = [4, 4]
        exp = [
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "X"]
        ]
        location = self.game.add_position(key, self.token)
        self.assertEqual(location, "CORNER")
        self.assertEqual(self.game.board.positions, exp)

    def test_edge(self):
        key = [1, 0]
        exp = [
            ["_", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]
        location = self.game.add_position(key, self.token)
        self.assertEqual(location, "EDGE")
        self.assertEqual(self.game.board.positions, exp)

    def test_diagonal_left_to_right(self):
        key = [1, 1]
        exp = [
            ["_", "_", "_", "_", "_"],
            ["_", "X", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]
        location = self.game.add_position(key, self.token)
        self.assertEqual(location, "DIAGONAL")
        self.assertEqual(self.game.board.positions, exp)

    def test_diagonal_right_to_left(self):
        key = [1, 3]
        exp = [
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "X", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]
        location = self.game.add_position(key, self.token)
        self.assertEqual(location, "DIAGONAL")
        self.assertEqual(self.game.board.positions, exp)


class TestResetGame(BaseTestCase):
    def setUp(self):
        super(TestResetGame, self).setUp()

        self.show_scoreboard = patch.object(Game, "show_scoreboard").start()
        self.start_game = patch.object(Game, "start_game").start()
        self.generate_board = patch.object(Board, "generate_board").start()
        self.change_token = patch.object(Player, "change_token").start()

    def test_base_case(self):
        user_input = ["Y"]
        exp = ["Game Over"]

        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                self.game.reset_game()

        resp = out.getvalue().split("\n")
        self.assertTrue(all(msg in resp for msg in exp))

        self.assertEqual(self.change_token.call_count, 2)
        self.assertTrue(self.generate_board.called)
        self.assertTrue(self.show_scoreboard.called)
        self.assertTrue(self.start_game.called)

    def test_exit(self):
        user_input = ["N"]
        exp = ["Game Over", "Thanks for playing!"]

        with patch('builtins.input', side_effect=user_input):
            with self.assertRaises(SystemExit):
                with captured_output() as out:
                    self.game.reset_game()

        resp = out.getvalue().split("\n")
        self.assertTrue(all(msg in resp for msg in exp))
        self.assertTrue(self.generate_board.called)
        self.assertFalse(self.show_scoreboard.called)
        self.assertFalse(self.start_game.called)


class TestShowScoreBoard(BaseTestCase):
    def setUp(self):
        super(TestShowScoreBoard, self).setUp()
        self.game.player1.wins = 3
        self.game.player2.wins = 1

    def test_base_case(self):
        exp = "\nScoreboard:\nToothless: 3\nHiccup: 1\n"
        with captured_output() as out:
            self.game.show_scoreboard()

        resp = out.getvalue()
        self.assertEqual(resp, exp)


