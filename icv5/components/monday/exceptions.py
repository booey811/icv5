class ColumnInput(Exception):
    def __init__(self, repair_name, attribute):
        """Raised when incompatible values are sent to a column value"""
        print("{} {}".format(repair_name, attribute))

class DropdownMethodError(Exception):
    """Raised when attempting to use an invalid methods for a dropdown
    Must be add or remove"""

    def __init__(self, repair_name, attribute):
        print("{} {}".format(repair_name, attribute))
