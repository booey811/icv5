from time import time

from moncli import ColumnType
from moncli.entities import create_column_value

from icv5.components.monday import boardItem, boardItems_inventory, column_keys, manage, exceptions


class FinancialWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False, webhook_payload=None):

        new_column_dictionary = column_keys.financial_wrapper

        super().__init__(webhook_payload)

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):
        return self


class FinancialBoardItem(FinancialWrapper):
    column_dictionary = column_keys.financial_item

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):
        if item_id:
            super().__init__(item_id, self, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self, blank_item=True)
        else:
            print('FinancialBoardItem INIT else route')

    def construct_repairs_profile(self):

        self.get_mainboard_item()

        repairs_dict = self.create_repairs_dict()

        inventory_codes = self.create_inventory_codes(repairs_dict)

        for code in inventory_codes:
            print(inventory_codes[code])
            print(code)

            try:
                inv_item = boardItems_inventory.InventoryRepairItem(
                    self.get_inventory_from_product_board(code, inventory_codes[code]).id
                )

            except exceptions.NoItemsFoundFromMondayClientSearch:
                # Create A Product & Halt Process
                self.parts_status.change_value('Failed')
                self.apply_column_changes()
                return False

            self.attach_repair_subitem(inv_item)

    def attach_repair_subitem(self, inventory_item):

        subitem = FinancialBoardSubItem(blank_item=True)

        url = 'https://icorrect.monday.com/boards/985177480/pulses/{}'.format(str(inventory_item.partboard_id.easy))

        subitem.part_url.change_value([str(inventory_item.partboard_id.easy), url])

        subitem.change_multiple_attributes(
            [
                ['sale_price', int(inventory_item.sale_price.easy)],
                ['supply_price', int(inventory_item.supply_price.easy)],
                ['quantity_used', 1],
                ['partboard_id', str(inventory_item.partboard_id.easy)]
            ],
            return_only=True
        )

        new_subitem = self.item.create_subitem(
            item_name=str(inventory_item.name),
            column_values=subitem.adjusted_values
        )

        return new_subitem

    def get_inventory_from_product_board(self, inventory_code, repair_name):

        col_val = create_column_value(
            id='combined_id',
            column_type=ColumnType.text,
            text=str(inventory_code)
        )
        col_val.value = '"{}"'.format(str(inventory_code))

        results = manage.Manager().get_board('inventory_parts').get_items_by_column_values(col_val)

        if len(results) == 0:
            raise exceptions.NoItemsFoundFromMondayClientSearch(inventory_code)

        elif len(results) > 1:
            raise exceptions.TooManyItemsFoundInProducts(repair_name, inventory_code, self)

        elif len(results) == 1:
            for pulse in results:
                return pulse

        else:
            print('FinancialItem.get_inventory_from_product_board else route')
            return False

    def create_inventory_codes(self, repairs_dict):

        colours = [
            'TrackPad',
            'Charging Port',
            'Headphone Jack',
            'Home Button',
            'Front Screen Universal',
            'Rear Glass',
            'Front Screen (LG)',
            'Front Screen (Tosh)',
            'Rear Housing'
        ]

        inventory_codes = {}

        for repair in repairs_dict:

            if repairs_dict[repair] in colours:
                code = '{}-{}-{}'.format(
                    self.main_item.device.ids[0],
                    repair,
                    self.main_item.colour.index
                )
                name = '{} {} {}'.format(
                    self.main_item.device.labels[0],
                    repairs_dict[repair],
                    self.main_item.colour.text
                )
            else:
                code = '{}-{}'.format(
                    self.main_item.device.ids[0],
                    repair
                )
                name = '{} {}'.format(
                    self.main_item.device.labels[0],
                    repairs_dict[repair],
                )

            inventory_codes[code] = name

        return inventory_codes

    def create_repairs_dict(self):

        repairs_dict_raw = dict(zip(self.main_item.repairs.ids, self.main_item.repairs.labels))

        return repairs_dict_raw

    def get_mainboard_item(self):
        self.main_item = FinancialMainBoardLinkItem(self.mainboard_id.easy)
        return self.main_item


class FinancialBoardSubItem(FinancialWrapper):

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):

        self.column_dictionary = column_keys.financial_subitem

        if item_id:
            super().__init__(item_id, self, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self, blank_item=True)
        else:
            print('FinancialBoardSubItem INIT else route')


class FinancialMainBoardLinkItem(boardItem.MondayWrapper):

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):

        self.column_dictionary = column_keys.financial_mainlink

        if item_id:
            super().__init__(webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(webhook_payload)
        else:
            print('FinancialBoardItem INIT else route')

        if not blank_item:
            self.set_client_and_item(self, item_id)

        self.set_attributes(self, self.column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


def test_module(item_id):
    from pprint import pprint as p

    start_time = time()

    finance = FinancialBoardItem(item_id)
    finance.construct_repairs_profile()



    print("--- %s seconds ---" % (time() - start_time))


test_module(1062544146)
