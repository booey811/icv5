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


class NotDevelopedError(Exception):

    def __init__(self, column_type):
        print("{} columns have not been developed fully yet".format(column_type))
