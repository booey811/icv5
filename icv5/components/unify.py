from pprint import pprint as p

import moncli

from icv5.components.monday import boardItems_main, boardItems_refurbs, boardItems_inventory, exceptions, manage
from icv5.components.phonecheck import phonecheck


class UnifiedObject:

    def __init__(self, webhook_data):
        self.webhook = webhook_data
        print(webhook_data)

        self.main_item = None
        self.refurb_item = None
        self.inv_items = []

        self.zendesk = None
        self.stuart = None
        self.vend = None
        self.phonecheck = None

    def create_monday_object(self, monday_id, board=None):
        item_types = {
            'main': boardItems_main.MainBoardItem,
            'inventory_order': boardItems_inventory.InventoryOrderItem,
            'inventory_screenrefurb': boardItems_inventory.InventoryScreenRefurbItem,
            'inventory_stock': boardItems_inventory.InventoryStockItem,
            'refurb_toplevel': boardItems_refurbs.RefurbTopLevelBoardItem,
            'refurb_received': boardItems_refurbs.RefurbReceivedItem,
            'refurb_tested': boardItems_refurbs.RefurbTestedItem,
            'refurb_repairing': boardItems_refurbs.RefurbRepairingItem,
            'refurb_selling': boardItems_refurbs.RefurbSellingItem,
            'refurb_final': boardItems_refurbs.RefurbFinalItem,
            'refurb_backlog': boardItems_refurbs.RefurbBacklogItem,
            'refurb_return': boardItems_refurbs.RefurbReturnItem,
            'refurb_purchasing': boardItems_refurbs.RefurbPurchasingItem
        }

        boardid_by_item = {
            '349212843': boardItems_main.MainBoardItem,
            '867934405': boardItems_inventory.InventoryStockItem,
            '868065293': boardItems_inventory.InventoryMappingItem,
            '925661179': None
        }

        if not board:
            object_to_return = boardid_by_item[str(self.webhook['event']['boardId'])](monday_id)
        else:
            object_to_return = item_types[board](monday_id)

        object_to_return.user_id = self.webhook['event']['userId']

        return object_to_return

    def collect_inventory_objects(self):

        def create_search_string(monday_object, repair_id, colour=True):

            device_tup = tuple([monday_object.device.ids[0]])
            repair_tup = tuple([repair_id])
            colour_tup = tuple([monday_object.colour.index])

            if colour:
                search = str(tuple([device_tup, repair_tup, colour_tup]))
            else:
                search = str(tuple([device_tup, repair_tup, ()]))

            return search

        def search_inventory_board(search_string):

            search_val.value = '"{}"'.format(search_string)

            results = inv_board.get_items_by_column_values(search_val)

            return results

        manager = manage.Manager()
        inv_board = manager.get_board('inventory_mappings')
        search_val = inv_board.get_column_value('text99')

        direct_links = {
            '35': '901008625',  # Tempered Glass
        }

        if not self.main_item:
            raise exceptions.SubObjectNotAvailable
        else:
            main_board_item = self.main_item

        for repair_code in main_board_item.repairs.ids:

            if str(repair_code) in direct_links:
                main_board_item.inventory_items.append(
                    boardItems_inventory.InventoryMappingItem(direct_links[str(repair_code)]))
                continue

            string = create_search_string(main_board_item, repair_code, colour=True)

            results = search_inventory_board(string)

            if len(results) < 1:
                new_string = create_search_string(main_board_item, repair_code, colour=False)
                new_results = search_inventory_board(new_string)
                if len(new_results) < 1:
                    raise exceptions.CannotFindRepairMapping(main_board_item, string)
                elif len(new_results) > 1:
                    raise exceptions.FoundTooManyRepairMappings(main_board_item, new_string)
                else:
                    for pulse in new_results:
                        main_board_item.inventory_items.append(boardItems_inventory.InventoryMappingItem(pulse.id))

            elif len(results) > 1:
                raise exceptions.FoundTooManyRepairMappings(main_board_item, string)

            else:
                for pulse in results:
                    main_board_item.inventory_items.append(boardItems_inventory.InventoryMappingItem(pulse.id))


test = UnifiedObject({'event': {'userId': 4251271}})

test.refurb_item = test.create_monday_object(971316040, 'refurb_received')

phonecheck = phonecheck.PhoneCheckResult(test.refurb_item.imei_sn.easy)

test.refurb_item.process_phonecheck_results(phonecheck)