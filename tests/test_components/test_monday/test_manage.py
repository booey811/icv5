import unittest

import pytest
import moncli

from icv5.components.monday.manage import Manager


@pytest.mark.basic
class TestManagerBasic(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()

    def test_create_client(self):
        for client in self.manager.client_credentials:
            with self.subTest(client=client):
                self.manager.create_client(client)

    def test_get_boards_with_system_client(self):
        for board in self.manager.board_ids:
            with self.subTest(name=board, id=self.manager.board_ids[board]):
                result = self.manager.get_board(board)
                self.assertIsInstance(result, moncli.entities.Board)

    def tearDown(self):
        pass


@pytest.mark.complex
class TestManagerComplex(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()

    def test_get_boards_with_error_client(self):
        for board in self.manager.board_ids:
            with self.subTest(name=board, id=self.manager.board_ids[board]):
                result = self.manager.get_board(board, client_name='error')
                self.assertIsInstance(result, moncli.entities.Board)

    def test_get_boards_with_emails_client(self):
        for board in self.manager.board_ids:
            with self.subTest(name=board, id=self.manager.board_ids[board]):
                result = self.manager.get_board(board, client_name='emails')
                self.assertIsInstance(result, moncli.entities.Board)
