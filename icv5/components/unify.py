from pprint import pprint

from icv5.components.monday import boardItems_main, boardItems_refurbs, boardItems_inventory, manage


class UnifiedObject():

    def __init__(self, webhook_data):
        self.webhook = webhook_data
        self.main_item = None
        self.inv_items = []
        self.zendesk = None
        self.stuart = None
        self.vend = None

    @staticmethod
    def create_monday_object(monday_id, item_type):
        item_types = {
            'main': boardItems_main.MainBoardItem,
            'inventory_order': boardItems_inventory.InventoryOrderItem,
            'inventory_screenrefurb': boardItems_inventory.InventoryItemScreenRefurb,
            'inventory_stock': boardItems_inventory.InventoryStockItem,
            'refurb_toplevel': boardItems_refurbs.TopLevelBoardItem
        }

        return item_types[item_type](monday_id)

