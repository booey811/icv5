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

    def create_inventory_log(self, log_type='main', financial_object=False, retry=False):

        count = 0
        info = self.create_inventory_info()

        for part_id in info['ids']:
            results = manage.Manager().search_board(
                board_id='984924063',
                column_type='text',
                column_id=boardItems_inventory.InventoryWrapper.new_column_dictionary['combined_id']['column_id'],
                value=str(part_id)
            )

            # No Results - Create A Product
            if len(results) == 0:
                new_product = boardItems_inventory.InventoryRepairItem(
                    self.create_product_item(part_id, info['names'][count], count).id
                )
                if log_type == 'main':
                    time.sleep(5)
                    repairboard_item = boardItems_inventory.InventoryRepairItem(new_product.id)
                    repairboard_item.complete.change_value('Trigger')
                    repairboard_item.apply_column_changes()
                    count += 1
                    continue
                elif log_type == 'financial' and financial_object:
                    financial_object.parts_status.change_value('Failed')
                    financial_object.subitems.delete_all_subitems()
                    raise exceptions.ProductBeingCreated(info['names'][count])

            # 1 Results - Check Out Stock
            elif len(results) == 1:
                for pulse in results:
                    repairboard_item = boardItems_inventory.InventoryRepairItem(pulse.id)
                    if log_type == 'financial' and financial_object:
                        subitem = boardItems_reporting.FinancialCreationSubItem()
                        if count > 0:
                            discounted = int(repairboard_item.sale_price.easy) - 10
                        else:
                            discounted = repairboard_item.sale_price.easy
                        subitem.change_multiple_attributes(
                            [
                                ['sale_price', repairboard_item.sale_price.easy],
                                ['supply_price', repairboard_item.supply_price.easy],
                                ['discounted_price', discounted],
                                ['quantity_used', 1]
                            ],
                            return_only=True
                        )
                        subitem.part_url.change_value(
                            [
                                repairboard_item.partboard_id.easy,
                                'https://icorrect.monday.com/boards/985177480/pulses/{}'.format(
                                    str(repairboard_item.id))
                            ]
                        )
                        new_subitem = financial_object.item.create_subitem(
                            item_name=repairboard_item.name,
                            column_values=subitem.adjusted_values
                        )
                        financial_object.parts_status.change_value('Complete')

                    else:
                        repairboard_item.complete.change_value('Trigger')
                        repairboard_item.apply_column_changes()

            else:
                print('MainBoardItem.create_inventory_log else route')

            count += 1

        if log_type == 'financial':
            return

        self.eod.change_value('Complete')
        self.apply_column_changes()

    def check_stock(self):

        repairs_info = self.create_inventory_info()
        repairs_board = manage.Manager().get_board('inventory_products')

        parts_info = {}
        update = ['STOCK CHECK\n\n']

        for repair_id in repairs_info['ids']:

            splitted = repair_id.split('-')

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
        if any(num < 5 for num in quantities):
            status = 'Low Stock'
            self.status.change_value('Error')
        elif any(num < 1 for num in quantities):
            status = 'No Stock'
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


        for product_item in products:
            name = str(product_item.name)
            quantity = int(product_item.quantity.easy)
            tracking = str(product_item.tracking.easy)
            parts_info[name] = {'quantity': quantity, 'tracking': tracking}
