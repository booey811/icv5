from icv5.components.monday import boardItem, column_keys, manage


class InventoryWrapper(boardItem.MondayWrapper):
    new_column_dictionary = column_keys.inventory_wrapper

    def __init__(self, item_id, parent_obj, blank_item=False, webhook_payload=None):

        super().__init__(webhook_payload=webhook_payload)

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**self.new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class InventoryRepairItem(InventoryWrapper):
    column_dictionary = column_keys.inventory_repair

    def __init__(self, item_id=None, blank_item=True):
        self.partboard_id = None
        self.quantity = None
        self.complete = None
        self.repair_label = None
        self.device_label = None
        self.colour = None
        self.colour_label = None
        self.colour_id = None
        self.repair_id = None
        self.device_id = None
        self.combined_id = None
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def adjust_stock(self, add=None, subtract=None):

        part = InventoryPartItem(str(self.partboard_id.easy))

        if not part.quantity.easy:
            quantity = 0
        else:
            quantity = int(part.quantity.easy)

        if add and subtract:
            raise CannotAddAndSubtract
        elif add:
            part.quantity.change_value(int(quantity) + int(add))
        elif subtract:
            part.quantity.change_value(int(quantity) - int(subtract))

        part.apply_column_changes()


class InventoryPartItem(InventoryWrapper):

    column_dictionary = column_keys.inventory_part

    def __init__(self, item_id=None, blank_item=True):
        self.quantity = None
        if item_id:
            super().__init__(item_id, self, blank_item=False)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class InventoryStockCountItem(InventoryWrapper):
    column_dictionary = column_keys.inventory_stock_count

    def __init__(self, item_id=None, webhook_payload=None, blank_item=True):
        self.count_status = None
        self.quantity_before = None
        self.current_quantity = None
        self.count_quantity = None
        self.parts_id = None
        if item_id:
            super().__init__(item_id, self, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def process_stock_count_deprecated(self):

        # Get pulses in group & Create List of Objects For Them
        if self.webhook_payload['event']['groupId'] == 'new_group26476':
            count_items = []
            for item in manage.Manager().get_board('inventory_stock_counts').get_group('new_group26476').get_items():
                count_items.append(InventoryStockCountItem(item.id))

            # Check to see if any duplicate part IDs
            parts_dict = {}
            for item in count_items:
                if item.parts_id.easy in parts_dict:
                    parts_dict[item.parts_id.easy]['count'] += int(item.count_quantity.easy)
                else:
                    parts_dict[item.parts_id.easy] = {
                        'count': int(item.count_quantity.easy),
                        'current': int(item.current_quantity.easy)
                    }

            # Add quantities to inventory
            for count_item in parts_dict:
                for result in self.cli_client.get_items(ids=[count_item], limit=1):
                    result.change_multiple_column_values(
                        {
                            'quantity': int(parts_dict[count_item]['count'])
                        }
                    )

            # Adjust Stock Counts status & values to desired value
            for item in count_items:
                item.change_multiple_attributes(
                    [
                        ['count_status', 'Added to Stock'],
                        ['quantity_before', int(item.current_quantity.easy)]
                    ]
                )

        else:
            print('"Count Status" Status adjusted outside of "New Count Group"')

    def process_stock_count(self):

        # Currently does not account for one part being counted multiple times,
        # the last value entered would be the one used to set stock

        # Create stock object
        stock_object = InventoryPartItem(self.parts_id.easy)
        quantity_before = stock_object.quantity.easy
        # Adjust Stock level
        stock_object.quantity.change_value(int(self.count_quantity.easy))
        # Adjust Stock Count Board Item

        self.quantity_before.change_value(quantity_before)

        self.count_status.change_value('Added to Stock')

        stock_object.apply_column_changes(verbose=True)
        self.apply_column_changes(verbose=True)


class CannotAddAndSubtract(Exception):

    def __init__(self):
        print('You have tried to ad and subtract from a stock item simultaneously')
