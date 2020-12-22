import copy
from pprint import pprint
import json

import moncli

import exceptions
from manage import manager


class ColumnWrapper:

    def __init__(self, repair_object, column_value, attribute):
        self.attribute = attribute
        self.repair_object = repair_object
        self.moncli_val = column_value
        self.id = column_value.id
        self.title = column_value.title


class StatusValue(ColumnWrapper):

    def __init__(self, repair_object, column_value, attribute):
        super().__init__(repair_object, column_value, attribute)

        self.text = column_value.text
        self.index = column_value.index

    def __repr__(self):
        return repr(self.text)

    def change_value(self, text=False, index=False, keep_original=False):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        if text:
            self.repair_object.adjusted_values[self.id] = {'label': text}
            return {self.id: {'label': text}}
        elif index:
            self.repair_object.adjusted_values[self.id] = {'index': index}
            return {self.id: {'index': index}}
        else:
            raise exceptions.ColumnInput(self.repair_object.name, self.attribute)


class TextValue(ColumnWrapper):

    def __init__(self, repair_object, column_value, attribute):
        super().__init__(repair_object, column_value, attribute)

        self.text = column_value.text

    def __repr__(self):
        return repr(self.text)

    def change_value(self, text):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        self.repair_object.adjusted_values[self.id] = text
        return {self.id: text}


class NumberValue(ColumnWrapper):

    def __init__(self, repair_object, column_value, attribute):
        super().__init__(repair_object, column_value, attribute)

        self.number = column_value.number
        self.text = str(column_value.number)

    def __repr__(self):
        return repr(self.number)

    def change_value(self, number):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        self.repair_object.adjusted_values[self.id] = number
        return {self.id: number}


class DropdownValue(ColumnWrapper):

    def __init__(self, repair_object, column_value, attribute):
        super().__init__(repair_object, column_value, attribute)
        ids_raw = json.loads(self.moncli_val.value)
        if ids_raw and self.moncli_val.text:
            self.ids = ids_raw['ids']
            self.labels = [label.strip() for label in self.moncli_val.text.split(',')]
        else:
            self.ids = []
            self.labels = []

    def __repr__(self):
        return repr(self.ids)

    def change_value(self, method, ids_list=False, labels_list=False):
        """
Allows changing of dropdown columns via the 'add', 'replace' or 'remove' methods

        :type method: str
        :type ids_list: list
        :type labels_list: list
        :param method: type of column difference required
        :param ids_list: list of ids to add or remove
        :param labels_list: list of labels to add or remove
        :return: dictionary of column id to value (ids/list: ids/list)
        """

        if ids_list:
            inner_key = 'ids'
            ori_val = self.ids
            input_val = ids_list
        elif labels_list:
            inner_key = 'labels'
            ori_val = self.labels
            input_val = labels_list
        else:
            raise exceptions.ColumnInput(self.repair_object.name, self.attribute)

        if method == 'add':
            result = ori_val + list(set(input_val) - set(ori_val))
            inner = {inner_key: result}
        elif method == 'remove':
            result = list(set(ori_val) - set(input_val))
            inner = {inner_key: result}
        elif method == 'replace':
            result = input_val
            inner = {inner_key: result}
        else:
            raise exceptions.DropdownMethodError(self.repair_object.name, self.attribute)

        self.repair_object.adjusted_values[self.id] = inner

        return {self.id: inner}

class DateValue(ColumnWrapper):

    def __init__(self, repair_object, column_value, attribute):
        super().__init__(repair_object, column_value, attribute)
        pass


class CheckboxValue(ColumnWrapper):

    def __init__(self, repair_object, column_value, attribute):
        super().__init__(repair_object, column_value, attribute)
        pass


class LinkValue(ColumnWrapper):

    def __init__(self, repair_object, column_value, attribute):
        super().__init__(repair_object, column_value, attribute)
        pass
