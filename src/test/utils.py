import unittest
from contextlib import contextmanager
from io import StringIO
import sys

from mock import patch
from src.board import Board
from src.game import Game
from src.player import Player


class BaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.addCleanup(patch.stopall)

    def setUp(self):
        self.board_3x3 = Board(3)
        self.board_5x5 = Board(5)
        self.game = Game()
        self.game.board = Board(3)
        self.game.player1 = Player("Toothless", "X")
        self.game.player2 = Player("Hiccup", "O")


"""
Used first answer from here:
https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
"""
@contextmanager
def captured_output():
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out
