import unittest

import pytest

from icv5.components.monday import boardItem, boardItems_inventory, boardItems_main, boardItems_refurbs
from icv5.components.monday.manage import Manager


@pytest.mark.develop
class TestItemMovement(unittest.TestCase):

    def setUp(self):
        self.manager = Manager()
        self.test_item = self.manager.get_board('main').add_item('test_multipleItems.TestItemMovement')

    def tearDown(self):
        self.test_item.delete()
