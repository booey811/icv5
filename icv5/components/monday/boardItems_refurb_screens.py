from time import time

from moncli import ColumnType
from moncli.entities import create_column_value

from icv5.components.monday import boardItem, boardItems_inventory, column_keys, manage, exceptions


class ScreenRefurbWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False, webhook_payload=None):

        new_column_dictionary = column_keys.screen_refurbs_wrapper

        super().__init__(webhook_payload)

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):
        return self


class ScreenRefurbMenuItem(ScreenRefurbWrapper):

    column_dictionary = column_keys.screen_refurbs_menu

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):
        if item_id:
            super().__init__(item_id, self, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self, blank_item=True)
        else:
            print('ScreenRefurbMenuItem INIT else route')


class ScreenRefurbOngoingItem(ScreenRefurbWrapper):

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):

        self.column_dictionary = column_keys.screen_refurbs_ongoing

        if item_id:
            super().__init__(item_id, self, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self, blank_item=True)
        else:
            print('ScreenRefurbOngoingItem INIT else route')

        self.final_quantity = int(self.starting_quantity.easy) - int(self.lcd_damage.easy) - int(self.re_runs.easy)

    def process_batch_completion(self, type):

        refurb_part_item = ScreenRefurbMenuItem(self.refurb_part_id.easy)

        if type == 'glassing':

            refurb_part_item.deglassed_stock.change_value(
                int(refurb_part_item.deglassed_stock.easy) - int(self.starting_quantity.easy)
            )

            stock_item = boardItems_inventory.InventoryPartItem(self.part_id.easy)

            stock_item.quantity.change_value(int(stock_item.quantity.easy) + int(self.final_quantity))

            stock_item.apply_column_changes()

        elif type == 'deglassing':

            refurb_part_item.refurbable_stock.change_value(
                int(refurb_part_item.refurbable_stock.easy) - int(self.starting_quantity.easy)
            )

            refurb_part_item.deglassed_stock.change_value(
                int(self.final_quantity) + int(refurb_part_item.deglassed_stock.easy)
            )

        else:
            print('ScreenRefurbOngoingItem.process_batch_completion INIT else route')
            return False

        refurb_part_item.apply_column_changes()
