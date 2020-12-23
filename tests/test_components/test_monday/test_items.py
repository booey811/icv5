from pprint import pprint

from icv5.components.monday import boardItems_inventory

def test_inventory_items():

    item = boardItems_inventory.InventoryOrderItem(930027628)

    item.item.get_column_values()

    for thing in item.item.column_values:
        print(thing.title)
        pprint(thing)

test_inventory_items()