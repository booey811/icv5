from datetime import datetime

from moncli import ColumnType
from moncli.entities import create_column_value

from icv5.components.monday import boardItem, column_keys, exceptions, manage, boardItems_inventory, boardItems_reporting



class EnquiryWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = column_keys.inventory_wrapper

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class GeneralEnquiryItem(EnquiryWrapper):

    column_dictionary = column_keys.enquiries_general

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)
            assert getattr(self, 'email'), NoEmailOnMonday(self)
            if not self.body.easy:
                self.body.easy = 'This Enquiry Is Blank On Monday'

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

class StuartDataItem(boardItem.MondayWrapper):

    column_dictionary = column_keys.stuart_data

    def __init__(self, item_id=None, blank_item=False):

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        self.set_attributes(self, self.column_dictionary)

        if blank_item:
            self.create_blank_item()

    @staticmethod
    def get_data_item(stuart_job_id):

        col_val = create_column_value(id='stuart_job_id', column_type=ColumnType.text, value=str(stuart_job_id))

        for pulse in manage.Manager().get_board('stuart_data_new').get_items_by_column_values(col_val):
            return StuartDataItem(pulse.id)

    def create_blank_item(self):

        return self

    def update_timings(self, direction):

        hour = datetime.now().hour
        min = datetime.now().minute

        if direction == 'collecting':
            self.collection_time.change_value([hour, min])
        elif direction == 'delivering':
            self.delivery_time.change_value([hour, min])
            self.status.change_value('Complete')

        self.apply_column_changes()


class WastageBoardItem(boardItem.MondayWrapper):

    column_dictionary = column_keys.wastage_item

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):

        super().__init__(webhook_payload=webhook_payload)

        if not blank_item:
            self.set_client_and_item(self, item_id)

        self.set_attributes(self, self.column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self

    def process_wastage(self):

        part_item = boardItems_inventory.InventoryPartItem(self.partboard_id.easy)

        new_quantity = part_item.adjust_stock(int(self.waste_quantity.easy))

        log = boardItems_reporting.InventoryMovementItem()

        log.change_multiple_attributes(
            [
                ['quantity_before', int(part_item.quantity.easy)],
                ['quantity_after', int(new_quantity)],
                ['product_id', str(part_item.id)],
                ['movement_type', 'OUT - Damaged']
            ],
            return_only=True
        )

        manage.Manager().get_board('inventory_movements').add_item(
            item_name=str(self.name),
            column_values=log.adjusted_values
        )

        self.waste_status.change_value('Complete')
        self.apply_column_changes()


class NoEmailOnMonday(Exception):

    def __init__(self, general_enquiry_item):
        print('No Email On Monday Which is Required To Process This Enquiry\n{}\n{}'.format(
            general_enquiry_item.name,
            general_enquiry_item.id
        ))
