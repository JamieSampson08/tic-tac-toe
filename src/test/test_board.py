from mock import patch
from src.board import Board
from src.test.utils import BaseTestCase


class TestBoardBase(BaseTestCase):
    def test_base_case(self):
        self.assertEqual(self.board_3x3.size, 3)
        self.assertEqual(self.board_3x3.positions, [])

    def test_init_position(self):
        exp = [
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"]
        ]
        self.board_3x3.init_positions()
        self.assertEqual(self.board_3x3.positions, exp)


class TestGenerateBoard(BaseTestCase):
    def setUp(self):
        super(TestGenerateBoard, self).setUp()
        self.board_3x3.positions = [
            ["X", "X", "X"],
            ["X", "X", "X"],
            ["X", "X", "X"]
        ]

    def test_help(self):
        exp = ("00 | 01 | 02\n"
               "10 | 11 | 12\n" 
               "20 | 21 | 22\n"
               )
        res = self.board_3x3.generate_board(help=True)
        self.assertEqual(res, exp)

    def test_positions(self):
        exp = ("X | X | X\n"
               "X | X | X\n"
               "X | X | X\n"
               )
        res = self.board_3x3.generate_board()
        self.assertEqual(res, exp)


class TestCheckIsWinningBoard(BaseTestCase):
    def setUp(self):
        super(TestCheckIsWinningBoard, self).setUp()
        self.keys = [1, 0]
        self.board_5x5.positions = [
            ["_", "_", "_"],
            ["O", "_", "_"],
            ["_", "_", "_"]
        ]

        # patch winning config functions
        self.check_horizontal = patch.object(Board, "check_horizontal").start()
        self.check_right_left_diagonal = patch.object(Board, "check_right_left_diagonal").start()
        self.check_vertical = patch.object(Board, "check_vertical").start()
        self.check_left_right_diagonal = patch.object(Board, "check_left_right_diagonal").start()

        self.check_horizontal.return_value = False
        self.check_right_left_diagonal.return_value = False
        self.check_left_right_diagonal.return_value = False
        self.check_vertical.return_value = False

    def test_base_case(self):
        self.check_vertical.return_value = True

        resp = self.board_5x5.check_is_winning_board("OTHER", self.keys)
        self.check_horizontal.assert_called_with(self.keys, "O")
        self.assertFalse(self.check_right_left_diagonal.called)
        self.assertFalse(self.check_left_right_diagonal.called)
        self.assertTrue(self.check_horizontal.called)
        self.assertTrue(self.check_vertical.called)
        self.assertTrue(resp)

    def test_location_edge_or_other(self):
        resp = self.board_5x5.check_is_winning_board("EDGE", self.keys)
        self.check_horizontal.assert_called_with(self.keys, "O")
        self.assertFalse(self.check_right_left_diagonal.called)
        self.assertFalse(self.check_left_right_diagonal.called)
        self.assertTrue(self.check_horizontal.called)
        self.assertTrue(self.check_vertical.called)
        self.assertFalse(resp)

    def test_location_not_edge_or_other(self):
        self.keys = [0, 0]
        self.board_5x5.positions = [
            ["O", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"]
        ]
        resp = self.board_5x5.check_is_winning_board("CORNER", self.keys)
        self.check_horizontal.assert_called_with(self.keys, "O")
        self.assertTrue(self.check_right_left_diagonal.called)
        self.assertTrue(self.check_vertical.called)
        self.assertTrue(self.check_left_right_diagonal.called)
        self.assertTrue(self.check_horizontal.called)
        self.assertFalse(resp)


class TestWinningConfigurations(BaseTestCase):
    def setUp(self):
        super(TestWinningConfigurations, self).setUp()
        self.keys = [0, 0]
        self.token = "X"

    def test_horizontal(self):
        self.board_5x5.positions = [
            ["X", "X", "X", "X", "X"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]
        resp = self.board_5x5.check_horizontal(self.keys, self.token)
        self.assertTrue(resp)

    def test_no_horizontal(self):
        self.board_5x5.positions = [
            ["X", "X", "X", "_", "X"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"]
        ]
        resp = self.board_5x5.check_horizontal(self.keys, self.token)
        self.assertFalse(resp)

    def test_vertical(self):
        self.board_5x5.positions = [
            ["X", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
        ]
        resp = self.board_5x5.check_vertical(self.keys, self.token)
        self.assertTrue(resp)

    def test_no_vertical(self):
        self.board_5x5.positions = [
            ["X", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
        ]
        resp = self.board_5x5.check_vertical(self.keys, self.token)
        self.assertFalse(resp)

    def test_right_left_diagonal(self):
        self.board_5x5.positions = [
            ["_", "_", "_", "_", "X"],
            ["_", "_", "_", "X", "_"],
            ["_", "_", "X", "_", "_"],
            ["_", "X", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
        ]
        resp = self.board_5x5.check_right_left_diagonal(self.token)
        self.assertTrue(resp)

    def test_no_right_left_diagonal(self):
        self.board_5x5.positions = [
            ["_", "_", "_", "_", "X"],
            ["_", "_", "_", "X", "_"],
            ["_", "_", "X", "_", "_"],
            ["_", "_", "_", "_", "_"],
            ["X", "_", "_", "_", "_"],
        ]
        resp = self.board_5x5.check_right_left_diagonal(self.token)
        self.assertFalse(resp)

    def test_left_right_diagonal(self):
        self.board_5x5.positions = [
            ["X", "_", "_", "_", "_"],
            ["_", "X", "_", "_", "_"],
            ["_", "_", "X", "_", "_"],
            ["_", "_", "_", "X", "_"],
            ["_", "_", "_", "_", "X"],
        ]
        resp = self.board_5x5.check_left_right_diagonal(self.token)
        self.assertTrue(resp)

    def test_no_left_right_diagonal(self):
        self.board_5x5.positions = [
            ["X", "_", "_", "_", "_"],
            ["_", "X", "_", "_", "_"],
            ["_", "_", "X", "_", "_"],
            ["_", "_", "_", "X", "_"],
            ["_", "_", "_", "_", "_"],
        ]
        resp = self.board_5x5.check_left_right_diagonal(self.token)
        self.assertFalse(resp)
