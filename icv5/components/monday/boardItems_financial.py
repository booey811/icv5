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

        self.disassemble_repairs_profile()
        self.get_mainboard_item()

        repairs_dict = self.create_repairs_dict()
        inventory_dict = self.create_inventory_codes(repairs_dict)

        stock_status = 'Do Now!'

        for code in inventory_dict:

            if code.split('-')[1] == '63':
                stock_status = 'Manual'

            try:
                inv_id = self.get_inventory_from_product_board(code, inventory_dict[code]).id
                inv_item = boardItems_inventory.InventoryRepairItem(inv_id)
                if self.be_generator.easy:
                    continue

            except exceptions.NoItemsFoundFromMondayClientSearch:
                # Create A Product & Halt Process
                self.create_repair_product(code, inventory_dict)
                if self.be_generator.easy:
                    continue
                self.parts_status.change_value('Failed - Creation')
                self.apply_column_changes()
                return False

            self.attach_repair_subitem(inv_item)

        if self.linked_client.easy == 'Refurb':
            stock_status = 'Manual'

        self.parts_status.change_value('Complete')
        self.stock_adjustment.change_value(stock_status)
        self.apply_column_changes()

    def attach_repair_subitem(self, inventory_item):

        subitem = FinancialBoardSubItem(blank_item=True)
        url = 'https://icorrect.monday.com/boards/985177480/pulses/{}'.format(str(inventory_item.partboard_id.easy))
        subitem.part_url.change_value([str(inventory_item.partboard_id.easy), url])

        if 'screen' in inventory_item.name or 'Screen' in inventory_item.name:
            prices = [
                [inventory_item.lcd.easy, 'G T & LCD'],
                [inventory_item.touch.easy, 'G & T'],
                [inventory_item.glass.easy, 'T'],
                [inventory_item.supply_price.easy, 'Bought Screen']
            ]
            supply_info = next((item for item in prices if item[0]), [0, 'No Supply Price'])
            supply_price = supply_info[0]
            name = '{}:{} - {}'.format(inventory_item.name, supply_info[1], self.main_item.refurb.easy)

        else:
            name = inventory_item.name
            supply_price = inventory_item.supply_price.easy


        subitem.change_multiple_attributes(
            [
                ['sale_price', round(float(inventory_item.sale_price.easy), 2)],
                ['supply_price', round(float(supply_price)), 2],
                ['quantity_used', 1],
                ['partboard_id', str(inventory_item.partboard_id.easy)],
                ['repair_credits', int(inventory_item.repair_credits.easy)]
            ],
            return_only=True
        )

        new_subitem = self.item.create_subitem(
            item_name=str(name),
            column_values=subitem.adjusted_values
        )

        return new_subitem

    def get_inventory_from_product_board(self, inventory_code, repair_details):

        repair_name = ' '.join([item for item in repair_details.values()])

        col_val = create_column_value(
            id='combined_id',
            column_type=ColumnType.text,
            text=str(inventory_code)
        )

        col_val.value = '"{}"'.format(str(inventory_code))

        results = manage.Manager().get_board('inventory_products').get_items_by_column_values(col_val)

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
            'Rear Housing',
            'Microphone'
        ]

        inventory_codes = {}

        for repair in repairs_dict:

            res_dict = {
                'device': self.main_item.device.labels[0],
                'repair': repairs_dict[repair],
            }

            if res_dict['repair'] in colours:

                code = '{}-{}-{}'.format(
                    self.main_item.device.ids[0],
                    repair,
                    self.main_item.colour.index
                )
                res_dict['colour'] = self.main_item.colour.easy

            else:
                code = '{}-{}'.format(
                    self.main_item.device.ids[0],
                    repair
                )

            inventory_codes[code] = res_dict

        return inventory_codes

    def create_repairs_dict(self):

        repairs_dict_raw = dict(zip(self.main_item.repairs.ids, self.main_item.repairs.labels))

        return repairs_dict_raw

    def get_mainboard_item(self):
        self.main_item = FinancialMainBoardLinkItem(self.mainboard_id.easy)
        return self.main_item

    def disassemble_repairs_profile(self):

        if self.subitems.easy:

            results = self.cli_client.get_items(ids=self.subitems.ids)

            for pulse in results:
                subitem = FinancialBoardSubItem(pulse.id)

                subitem.void_financial_entry()

    def create_repair_product(self, inventory_code, inventory_dict):

        inv_item = boardItems_inventory.InventoryRepairItem(blank_item=True)

        inv_code_list = inventory_code.split('-')

        device_id = inv_code_list[0]
        repair_id = inv_code_list[1]

        atts_to_change = [
            ['device_id', str(device_id)],
            ['repair_id', str(repair_id)],
            ['device_label', str(inventory_dict[inventory_code]['device'])],
            ['repair_label', str(inventory_dict[inventory_code]['repair'])],
            ['combined_id', inventory_code],
            ['dual_only_id', '{}-{}'.format(device_id, repair_id)]
        ]

        product_name = '{} {}'.format(
            inventory_dict[inventory_code]['device'],
            inventory_dict[inventory_code]['repair']
        )

        if len(inv_code_list) == 3:
            atts_to_change.append(['colour_id', str(inv_code_list[2])])
            atts_to_change.append(['colour_label', str(inventory_dict[inventory_code]['colour'])])
            atts_to_change.append(['colour', str(inventory_dict[inventory_code]['colour'])])
            product_name = '{} {} {}'.format(
                inventory_dict[inventory_code]['device'],
                inventory_dict[inventory_code]['repair'],
                inventory_dict[inventory_code]['colour']
            )

        inv_item.change_multiple_attributes(
            atts_to_change,
            return_only=True
        )

        new_inventory = manage.Manager().get_board('inventory_products').add_item(
            item_name=product_name.replace('"', ' inch'),
            column_values=inv_item.adjusted_values
        )

        return new_inventory

    def stock_deductions_and_recording(self):

        for item_id in self.subitems.ids:
            subitem = FinancialBoardSubItem(item_id=item_id)

            subitem.process_stock_adjustment(self)


class FinancialBoardSubItem(FinancialWrapper):

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):

        self.column_dictionary = column_keys.financial_subitem

        if item_id:
            super().__init__(item_id, self, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self, blank_item=True)
        else:
            print('FinancialBoardSubItem INIT else route')

    def process_stock_adjustment(self, parent_item):

        part_item = boardItems_inventory.InventoryPartItem(self.partboard_id.easy)

        quantity_to_change = int(self.quantity_used.easy)

        if quantity_to_change == 0 or not quantity_to_change:
            print('No Parts Used For This Repair')
            self.item.add_update('No Parts Used in This Repair')
            new_quantity = old_quantity = int(part_item.quantity.easy)
            movement_type = 'No Parts Used'
        else:
            new_quantity = part_item.adjust_stock(quantity_to_change)
            old_quantity = int(part_item.quantity.easy)
            movement_type = 'OUT - iCorrect'

        inv = FinancialInventoryMovementItem(blank_item=True)

        inv.generate_inventory_item_fields(
            part_item=part_item,
            old_quantity=old_quantity,
            new_quantity=new_quantity,
            parent_item=parent_item,
            movement_type=movement_type
        )

        movement = manage.Manager().get_board('inventory_movements').add_item(
            item_name=part_item.name.replace('"', ''),
            column_values=inv.adjusted_values
        )

        self.change_multiple_attributes(
            [
                ['eod_status', 'Complete'],
                ['movementboard_id', str(movement.id)]
            ],
            return_only=True
        )

        self.movement_url.change_value(
            [
                str(movement.id),
                'https://icorrect.monday.com/boards/989490856/pulses/{}'.format(str(movement.id))
            ]
        )

        self.apply_column_changes()

    def void_financial_entry(self):

        if int(self.quantity_used.easy) == 0:
            pass
        elif not self.quantity_used.easy:
            pass
        elif self.partboard_id.easy and self.eod_status.easy == 'Complete':
            self.reverse_stock_changes()
        else:
            print('FinancialSubItem.void_financial_entry else route')

        self.item.delete()

    def reverse_stock_changes(self):

        part_item = boardItems_inventory.InventoryPartItem(self.partboard_id.easy)

        current_quantity = int(part_item.quantity.easy)
        used_quantity = -int(self.quantity_used.easy)
        new_quantity = current_quantity - used_quantity

        part_item.adjust_stock(used_quantity)

        inv = FinancialInventoryMovementItem(blank_item=True)

        inv.generate_inventory_item_fields(
            part_item,
            current_quantity,
            new_quantity,
            movement_type='IN - Void'
        )

        movement_item = manage.Manager().get_board('inventory_movements').add_item(
            item_name=self.name,
            column_values=inv.adjusted_values
        )


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


class FinancialInventoryMovementItem(boardItem.MondayWrapper):

    def __init__(self, item_id=None, webhook_payload=None, blank_item=False):

        self.column_dictionary = column_keys.inventory_movement

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

    def generate_inventory_item_fields(self, part_item, old_quantity, new_quantity, parent_item=None, movement_type=None):

        movement_types = [
            'OUT - iCorrect',
            'OUT - Refurb',
            'OUT - Damaged',
            'OUT - Return',
            'IN - Order',
            'IN - Refurbished Screen',
            'IN - Void',
            'No Parts Used'
        ]

        if movement_type not in movement_types:
            raise exceptions.InvalidMovementType(movement_type)

        atts_to_change = [
            ['quantity_before', int(old_quantity)],
            ['quantity_after', int(new_quantity)],
            ['movement_type', str(movement_type)],
            ['device_label', str(part_item.device_label.easy)],
            ['repair_label', str(part_item.repair_label.easy)],
            ['colour_label', str(part_item.colour_label.easy)],
            ['device_id', str(part_item.device_id.easy)],
            ['repair_id', str(part_item.repair_id.easy)],
            ['colour_id', str(part_item.colour_id.easy)]
        ]

        if parent_item:
            atts_to_change.append(['mainboard_name', str(parent_item.name)])
            atts_to_change.append(['mainboard_id', str(parent_item.id)])

        self.change_multiple_attributes(
            atts_to_change,
            return_only=True
        )

        self.part_url.change_value(
            [str(part_item.id), 'https://icorrect.monday.com/boards/985177480/pulses/{}'.format(str(part_item.id))]
        )

