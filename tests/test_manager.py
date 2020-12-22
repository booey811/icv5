import pytest

from icv5.components.monday.manage import manager
from icv5.components.monday import boardItem, boardItems_main, boardItems_refurbs

def test_create_client(client=False):
    manager.create_client(client)


def test_all_client_creation():
    for client in manager.client_credentials:
        print(client)
        test_create_client(client)

def test_create_blank_object_from_main_to_refurb_top():
    ori = boardItems_main.MainBoardItem(926422006)
    new = boardItem.TranslationObject('refurb_toplevel', ori)