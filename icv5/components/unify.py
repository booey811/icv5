import moncli

from icv5.components.monday import boardItems_main, boardItems_refurbs, boardItems_inventory, exceptions


class UnifiedObject:

    def __init__(self, webhook_data):
        self.webhook = webhook_data
        self.main_item = None
        self.inv_items = []
        self.zendesk = None
        self.stuart = None
        self.vend = None

    def create_monday_object(self, monday_id, board=None):
        item_types = {
            'main': boardItems_main.MainBoardItem,
            'inventory_order': boardItems_inventory.InventoryOrderItem,
            'inventory_screenrefurb': boardItems_inventory.InventoryScreenRefurbItem,
            'inventory_stock': boardItems_inventory.InventoryStockItem,
            'refurb_toplevel': boardItems_refurbs.TopLevelBoardItem
        }

        boardid_by_item = {
            '349212843': boardItems_main.MainBoardItem,
            '867934405': boardItems_inventory.InventoryStockItem,
            '868065293': None,  # To be changed to repair mapping item
            '925661179': None
        }

        if not board:
            object_to_return = boardid_by_item[str(self.webhook['event']['boardId'])](monday_id)
        else:
            object_to_return = item_types[board](monday_id)

        object_to_return.user_id = self.webhook['event']['userId']

        return object_to_return

    def collect_inventory_objects(self):

        direct_links = {
            '35': '901008625',  # Tempered Glass
        }

        if not self.main_item:
            raise exceptions.SubObjectNotAvailable
        else:
            item = self.main_item

        print(item.repairs)

        for rep_index in item.repairs.ids:
            # Filter out items that do not require a device
            if str(rep_index) in direct_links:
                item.inventory_items.append(boardItems_inventory.InventoryMappingItem(direct_links[str(rep_index)]))
            else:
                device_tup = (item.device.ids[0],)
                repair_tup = (rep_index,)
                colour_tup = (item.colour.index,)
                search1 = (device_tup, repair_tup, colour_tup)
                search_val = moncli.create_column_value(id='text99', column_type=moncli.ColumnType.text,
                                                        value=str(search1))
                results = item.client.get_board('inventory_mappings').get_items_by_column_value(search_val)

                if len(results) == 0:
                    search2 = (device_tup, repair_tup)
                    search_val = moncli.create_column_value(id='text99', column_type=moncli.ColumnType.text,
                                                            value=str(search2))
                    results = item.client.get_board('inventory_mappings').get_items_by_column_value(search_val)

                    if len(results) == 0:
                        raise exceptions.CannotFindRepairMapping(item, search1, 'error')

                    elif len(results) > 1:
                        pass
                        # Raise an exception

test = UnifiedObject({
    'event': {
        'app': 'monday',
        'boardId': 349212843,
        'userId': 4251271
    }
})

test.main_item = test.create_monday_object(894201398)

test.collect_inventory_objects()

print(test.main_item.inventory_items)
