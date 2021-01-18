import unittest

import pytest

@pytest.fixture
def attributes_to_test():
    return ['status', 'imei', 'device']



def test_change_status_value(blank_main_object, attributes_to_test):

    # Take blank object from conftest and do stuff
    pass