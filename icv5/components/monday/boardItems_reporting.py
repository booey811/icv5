from pprint import pprint as p
import time

from icv5.components.monday import boardItem, column_keys, boardItems_inventory, boardItems_main, exceptions, manage


class ReportingWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = column_keys.reporting_wrapper

        super().__init__()

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self


class InventoryMovementItem(ReportingWrapper):
    column_dictionary = column_keys.inventory_movement

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def remove_stock(self):
        try:
            quantity = int(self.quantity.easy)
        except ValueError:
            quantity = 0
        new_quantity = quantity - 1
        self.quantity_before.change_value(quantity)
        self.quantity_after.change_value(new_quantity)
        self.adjust_parts_item(new_quantity)
        self.apply_column_changes()

    def adjust_parts_item(self, new_quantity):
        parts_item = boardItems_inventory.InventoryPartItem(self.partboard_id.easy)
        parts_item.quantity.change_value(new_quantity)
        parts_item.apply_column_changes()


class FinancialCreationItem(ReportingWrapper):
    column_dictionary = column_keys.reporting_financial

    def __init__(self, item_id=None, blank_item=True):
        self.mainboard_id = None
        if item_id:
            super().__init__(item_id, self)

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def add_repair_subitems(self):
        main_item = boardItems_main.MainBoardItem(self.mainboard_id.easy)
        try:
            main_item.create_inventory_log('financial', financial_object=self)
        except exceptions.ProductBeingCreated:
            self.parts_status.change_value('Failed')
            self.subitems.delete_all_subitems()
        finally:
            self.apply_column_changes()


class FinancialItem(ReportingWrapper):
    column_dictionary = column_keys.reporting_financial

    def __init__(self, item_id=None, main_item=None, blank_item=True):
        self.mainboard_id = None
        self.main_item = main_item
        if item_id:
            super().__init__(item_id, self)

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def process_repair_data(self):

        self.main_item = boardItems_main.MainBoardItem(item_id=str(self.mainboard_id.easy))

        count = 0
        info = self.create_inventory_info(self.main_item)

        for part_id in info['ids']:
            results = manage.Manager().search_board(
                board_id='984924063',
                column_type='text',
                column_id=boardItems_inventory.InventoryWrapper.new_column_dictionary['combined_id']['column_id'],
                value=str(part_id)
            )

            if len(results) == 0:
                new_item = self.create_product_item(self.main_item, part_id, info['names'][count], count)
                product = boardItems_inventory.InventoryRepairItem(new_item.id)

            elif len(results) == 1:
                for item in results:
                    product = boardItems_inventory.InventoryRepairItem(item.id)

            else:
                raise exceptions.TooManyItemsFoundInProducts(info['names'][count], part_id, self)

            self.add_repair_subitem(product)

    def add_repair_subitem(self, product):
        # Add Subitem
        subitem = FinancialSubItem()

        subitem.change_multiple_attributes(
            [
                ['sale_price', product.sale_price.easy],
                ['supply_price', product.supply_price.easy],
                ['quantity_used', 1]
            ],
            return_only=True
        )
        subitem.part_url.change_value(
            [
                product.partboard_id.easy,
                'https://icorrect.monday.com/boards/985177480/pulses/{}'.format(str(product.id))
            ]
        )

        new_subitem = self.item.create_subitem(
            item_name=product.name,
            column_values=subitem.adjusted_values
        )

        return new_subitem

    def create_inventory_log(self, log_type='main', financial_object=False, retry=False):

        self.main_item = boardItems_main.MainBoardItem(str(self.mainboard_id))

        count = 0
        info = self.create_inventory_info(self.main_item)

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
                    self.create_product_item(self.main_item, part_id, info['names'][count], count).id
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
                        subitem = FinancialSubItem()
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

    @staticmethod
    def create_product_item(main_item, part_id, name, count):
        name = name.replace('"', ' Inch')
        new_product_item = boardItems_inventory.InventoryRepairItem()
        id_split = part_id.split('-')
        new_product_item.combined_id.change_value(part_id)
        new_product_item.device_id.change_value(str(id_split[0]))
        new_product_item.repair_id.change_value(str(id_split[1]))
        if len(id_split) == 3:
            new_product_item.colour_id.change_value(str(id_split[2]))
            new_product_item.colour_label.change_value(str(main_item.colour.easy))
            new_product_item.colour.change_value(str(main_item.colour.easy))
        new_product_item.device_label.change_value(str(main_item.device.easy[0]))
        new_product_item.repair_label.change_value(str(main_item.repairs.easy[count]))

        created_item = manage.Manager().get_board('inventory_products').add_item(
            item_name=name,
            column_values=new_product_item.adjusted_values
        )
        return created_item

    @staticmethod
    def create_inventory_info(main_item):

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
        for repair in main_item.repairs.ids:
            if main_item.repairs.labels[id_count] in colours:
                ids.append('{}-{}-{}'.format(main_item.device.ids[0], repair, main_item.colour.index))
            else:
                ids.append('{}-{}'.format(main_item.device.ids[0], repair, main_item.colour.index))
            id_count += 1

        name_count = 0
        for repair in main_item.repairs.easy:
            if main_item.repairs.labels[name_count] in colours:
                names.append('{} {} {}'.format(main_item.device.easy[0], repair, main_item.colour.easy))
            else:
                names.append('{} {}'.format(main_item.device.easy[0], repair))
            name_count += 1

        return {'ids': ids, 'names': names}


class FinancialSubItem(ReportingWrapper):
    column_dictionary = column_keys.reporting_financial_sub

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class FinancialCreationSubItem(ReportingWrapper):
    column_dictionary = column_keys.reporting_financial_sub

    def __init__(self, item_id=None, blank_item=True):
        if item_id:
            super().__init__(item_id, self)

        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)
