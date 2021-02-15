from icv5.components.monday import manage


class ColumnInput(Exception):
    def __init__(self, repair_name, attribute):
        """Raised when incompatible values are sent to a column value"""
        print("{} {}".format(repair_name, attribute))


class DropdownMethodError(Exception):
    """Raised when attempting to use an invalid methods for a dropdown
    Must be add or remove"""

    def __init__(self, repair_name, attribute):
        print("{} {}".format(repair_name, attribute))


class NoBoardFound(Exception):
    """Raised when attempting to search for a board that cannot be found"""

    def __init__(self, board_id, board_name=False):
        if board_name:
            string = 'No Board found with ID: {} and Name: {}'.format(board_id, board_name)
        else:
            string = 'No Board found with ID: {}'.format(board_id)
        print(string)


class BoardItemArgumentError(Exception):

    def __init__(self):
        print('Unable to create boardItem, an item ID or the "blank_item" arguments must be given')


class SubObjectNotAvailable(Exception):

    def __init__(self, parent_object, object_to_attach):
        print(
            '{} Object has not been created so {} Object cannot be added to it'.format(parent_object, object_to_attach))


class NotDevelopedError(Exception):

    def __init__(self, column_type):
        print("{} columns have not been developed fully yet".format(column_type))


class CannotFindRepairMapping(Exception):

    def __init__(self, monday_object, code_string):
        print('Unable to find this repair on Repair Mappings Board')

        manage.Manager().add_update(
            item_object=monday_object.item,
            user_id=monday_object.user_id,
            client='error',
            update='Cannot Find Repair Mapping For {}'.format(code_string),
            notify=['Cannot Find Repair Mapping For {}'.format(code_string), 4251271]
        )


class FoundTooManyRepairMappings(Exception):

    def __init__(self, monday_object, code_string):
        print('Unable to find this repair on Repair Mappings Board')

        manage.Manager().add_update(
            item_object=monday_object.item,
            user_id=monday_object.user_id,
            client='error',
            update='Too Many Repair Mappings Found For {}'.format(code_string),
            notify=['Too Many Repair Mappings Found For {}'.format(code_string), 4251271]
        )


class IncorrectCodeTypeRequest(Exception):

    def __init__(self, code_type):
        print('The available options for this function are "unit" or "batch", you have selected "{}"'.format(code_type))


class NoItemsFoundFromMondayClientSearch(Exception):

    def __init__(self, search_value):
        print('Unable to find item with ID {}'.format(search_value))


class ProductBeingCreated(Exception):

    def __init__(self, name):

        print('This Product-Repair is Being Created: {}'.format(name))


class TooManyItemsFoundInProducts(Exception):

    def __init__(self, name, part_id, finance_item):
        print('Too Many Products Found for {}\n\nPart ID: {}'.format(name, part_id))
        finance_item.parts_status.change_value('Failed')
        finance_item.item.add_update('Too Many Products Found for {}\n\nPart ID: {}'.format(name, part_id))
