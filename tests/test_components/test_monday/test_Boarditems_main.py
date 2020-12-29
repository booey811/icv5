import unittest

import pytest

from icv5.components.monday import boardItem, boardItems_inventory, boardItems_main, boardItems_refurbs
from icv5.components.monday.manage import Manager


@pytest.mark.develop
class TestMainBoardItems(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        pass

    def test_main_board_blank_item(self):
        blank_item = boardItems_main.MainBoardItem(blank_item=True)

    def test_add_blank_item_to_main_and_delete(self):
        blank_item = boardItems_main.MainBoardItem(blank_item=True)
        monday_item = self.manager.get_board('main').add_item(item_name='test_MainBoardItems')
        monday_item.delete()

    def test_add_arbitrary_item_to_main(self):
        blank_item = boardItems_main.MainBoardItem(blank_item=True)
