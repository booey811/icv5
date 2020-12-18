import pytest

from icv5.components.monday.manage import Manager


def test_client_creation():
    for client in Manager.client_credentials:
        Manager.create_client(client)

test_client_creation()