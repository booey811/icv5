import pytest


@pytest.fixture()
def blank_main_object():
    from icv5.components.monday.boardItems_main import MainBoardItem
    return MainBoardItem()


@pytest.fixture()
def return_gabe_user_id():
    return '4251271'


@pytest.fixture()
def return_sample_webhook_payload():
    return {'event': {'userId': '4251271'}}
