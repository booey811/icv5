import unittest

import pytest



@pytest.mark.offline
class TestMondayObjectColumnChanges(unittest.TestCase):

    @pytest.mark.usefixtures('blank_object_for_columns_tests')
    @staticmethod
    def test_change_status_value_by_label(blank_object_for_columns_tests):

        changed_value = blank_object_for_columns_tests.status.change_value('Adjusted in change by status')
        assert changed_value == {'statu': {'label': 'Adjusted in change by status'}}


