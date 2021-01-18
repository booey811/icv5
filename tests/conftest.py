import pytest


@pytest.fixture()
def blank_main_object():
    from icv5.components.monday.boardItems_main import MainBoardItem

    return MainBoardItem()
