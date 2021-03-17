import time

import moncli

from icv5.components.monday import boardItem, exceptions, column_keys, manage, boardItems_inventory, \
    boardItems_reporting


class MainBoardWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj_columns, blank_item=None, webhook_payload=None):

        new_column_dictionary = column_keys.main_wrapper

        super().__init__(webhook_payload)

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj_columns}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):
        return self


class MainBoardItem(MainBoardWrapper):
    column_dictionary = column_keys.main_item

    def __init__(self, item_id=None, webhook_payload=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self.column_dictionary, webhook_payload=webhook_payload)
        elif blank_item:
            super().__init__(None, self.column_dictionary, blank_item=True)
        else:
            raise exceptions.BoardItemArgumentError

        self.product_codes = {}

    def create_inventory_info(self):


        """MAKE AN OPTION TO CHECK STOCK ONLY WHICH RETRNS THE INVENTOIRY ITEMS THEMSELVES"""

        ids = []
        names = []
        colours = {
            'TrackPad',
            'Charging Port',
            'Headphone Jack',
            'Home Button',
            'Front Screen Universal',
            'Rear Glass',
            'Front Screen (LG)',
            'Front Screen (Tosh)',
            'Rear Housing'
        }

        id_count = 0
        for repair in self.repairs.ids:
            if self.repairs.labels[id_count] in colours:
                ids.append('{}-{}-{}'.format(self.device.ids[0], repair, self.colour.index))
            else:
                ids.append('{}-{}'.format(self.device.ids[0], repair, self.colour.index))
            id_count += 1

        name_count = 0
        for repair in self.repairs.easy:
            if self.repairs.labels[name_count] in colours:
                names.append('{} {} {}'.format(self.device.easy[0], repair, self.colour.easy))
            else:
                names.append('{} {}'.format(self.device.easy[0], repair))
            name_count += 1

        return {'ids': ids, 'names': names}

    def create_product_item(self, part_id, name, count):

        name = name.replace('"', ' Inch')
        new_product_item = boardItems_inventory.InventoryRepairItem()
        id_split = part_id.split('-')
        new_product_item.combined_id.change_value(part_id)
        new_product_item.device_id.change_value(str(id_split[0]))
        new_product_item.repair_id.change_value(str(id_split[1]))
        if len(id_split) == 3:
            new_product_item.colour_id.change_value(str(id_split[2]))
            new_product_item.colour_label.change_value(str(self.colour.easy))
            new_product_item.colour.change_value(str(self.colour.easy))
        new_product_item.device_label.change_value(str(self.device.easy[0]))
        new_product_item.repair_label.change_value(str(self.repairs.easy[count]))
        new_product_item.dual_only_id.change_value('{}-{}'.format(self.device_id.easy, self.repair_id.easy))

        created_item = manage.Manager().get_board('inventory_products').add_item(
            item_name=name,
            column_values=new_product_item.adjusted_values
        )
        return created_item

    def check_stock(self):

        repairs_info = self.create_inventory_info()
        repairs_board = manage.Manager().get_board('inventory_products')

        parts_info = {}
        update = ['STOCK CHECK\n\n']

        untracked = [
            '35',  # Tempered Glass
            '72',  # Liq Dam
            '99',  # Face ID
            '11',  # Apple Boot
            '37',  # Logic Board
            '10',  # Audio IC
        ]

        for repair_id in repairs_info['ids']:

            splitted = repair_id.split('-')

            if splitted[1] in untracked:
                continue

            if len(splitted) == 3:
                search = '{}-{}'.format(splitted[0], splitted[1])
            else:
                search = repair_id

            col_val = moncli.entities.create_column_value(
                id='dual_only_id',
                column_type=moncli.ColumnType.text,
                text=str(search)
            )

            col_val.value = '"{}"'.format(str(search))

            results = repairs_board.get_items_by_column_values(col_val)

            if len(results) == 0:
                raise exceptions.CannotFindRepairProduct(self, repair_id)

            elif len(results) > 0:
                self.process_stock_check_results(results, parts_info, repairs_board)

            else:
                print('MainItem.check_stock else route')
                return False

        for repair in parts_info:
            update.append(
                '{} (Tracking: {}) == {}'.format(
                    repair.replace('"', ''),
                    parts_info[repair]['tracking'],
                    parts_info[repair]['quantity']
                )
            )

        quantities = [parts_info[item]['quantity'] for item in parts_info]
        if any(num < 1 for num in quantities):
            status = 'No Stock'
            self.status.change_value('Error')
        elif any(num < 5 for num in quantities):
            status = 'Low Stock'
            self.status.change_value('Error')
        elif all(num > 4 for num in quantities):
            status = 'Stock Available'
        else:
            status = 'Error'

        if status not in ['Stock Available', 'Error']:
            manage.Manager().add_update(
                self,
                update='\n'.join(update),
                notify=[
                    "{}\nWe may not have the required stock for this repair, please click me and check!".format(
                        self.name
                    ),
                    self.user_id
                ]
            )

        else:
            manage.Manager().add_update(
                self,
                update='\n'.join(update),
            )

        self.be_stock_checker.change_value(status)
        self.apply_column_changes()

    def process_stock_check_results(self, results, parts_info, repairs_board):

        colours = {
            'TrackPad',
            'Charging Port',
            'Headphone Jack',
            'Home Button',
            'Front Screen Universal',
            'Rear Glass',
            'Front Screen (LG)',
            'Front Screen (Tosh)',
            'Rear Housing'
        }

        products = []

        for pulse in results:
            products.append(boardItems_inventory.InventoryRepairItem(pulse.id))

        parts = []
        for product_item in products:
            part_id = str(product_item.partboard_id.easy)
            if part_id in parts:
                continue
            else:
                name = str(product_item.name)
                quantity = int(product_item.quantity.easy)
                tracking = str(product_item.tracking.easy)
                parts_info[name] = {'quantity': quantity, 'tracking': tracking, 'part_id': part_id}
                parts.append(part_id)
