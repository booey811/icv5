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

    def generate_batch(self, refurb_phase):

        config = {
            'glassing': {
                'phase': 'Glassing',

            }
        }

        batch_board = manage.Manager().get_board('refurb_batches')

        parent_item_gen = ScreenRefurbOngoingItem(blank_item=True)

        parent_item_gen.change_multiple_attributes(
            [
                ['combined_id', str(self.combined_id.easy)],
                ['device_id', str(self.device_id.easy)],
                ['repair_id', str(self.repair_id.easy)],
                ['colour_id', str(self.colour_id.easy)],
                ['device_label', str(self.device_label.easy)],
                ['repair_label', str(self.repair_label.easy)],
                ['colour_label', str(self.colour_label.easy)],
                ['part_id', str(self.part_id.easy)],
                ['']
            ],
            return_only=True
        )

        parent_item = batch_board.add_item(
            item_name=self.name,
            column_values=parent_item_gen.adjusted_values
        )

        count = 1
        while count <= int(self.batch_size.easy):
            subitem_gen = ScreenRefurbOngoingSubItem(blank_item=True)
            subitem_gen.change_multiple_attributes(
                [
                    ['part_id', str(self.part_id.easy)],
                ],
                return_only=True
            )
            parent_item.create_subitem(
                item_name=self.name,
                column_values=subitem_gen.adjusted_values
            )
            count += 1


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

    def process_batch_completion(self, refurb_type):

        refurb_part_item = ScreenRefurbMenuItem(self.refurb_part_id.easy)

        if refurb_type == 'glassing':

            refurb_part_item.deglassed_stock.change_value(
                int(refurb_part_item.deglassed_stock.easy) - int(self.starting_quantity.easy)
            )

            if int(self.re_runs.easy) > 0:
                refurb_part_item.refurbable_stock.change_value(
                    int(refurb_part_item.refurbable_stock.easy) + int(self.re_runs.easy))

            stock_item = boardItems_inventory.InventoryPartItem(self.part_id.easy)

            stock_item.quantity.change_value(int(stock_item.quantity.easy) + int(self.final_quantity))

            stock_item.apply_column_changes()

        elif refurb_type == 'deglassing':

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

    def process_batch_completion_new(self):
        success = 0
        binned = 0
        re_run = 0
        for subitem_id in self.sub_item_ids.ids:
            screen = ScreenRefurbOngoingSubItem(item_id=subitem_id)
            if screen.final_result.easy == 'Successful':
                success += 1
            elif screen.final_result.easy == 'Binned':
                binned += 1
            elif screen.final_result.easy == 'Re-Started':
                re_run += 1
            else:
                print('ScreenRefurbOngoingItem.process_batch_completion')




class ScreenRefurbOngoingSubItem(ScreenRefurbWrapper):

    column_dictionary = column_keys.screen_refurbs_ongoing_subitem

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):
        if item_id:
            super().__init__(item_id, self, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self, blank_item=True)
        else:
            print('ScreenRefurbOngoingSubItem INIT else route')


