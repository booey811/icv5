import json

from icv5.components.monday import exceptions, manage


class ColumnWrapper:

    def __init__(self, repair_object, attribute, column_value):

        self.return_value = self
        self.attribute = attribute
        self.repair_object = repair_object
        self.moncli_val = None

        if isinstance(column_value, str):
            self.id = column_value

        else:
            self.moncli_val = column_value
            self.id = column_value.id
            self.title = column_value.title


class StatusValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if isinstance(column_value, str):
            self.text = None
            self.index = None
        else:
            self.text = column_value.text
            if json.loads(self.moncli_val.value):
                self.index = column_value.index
            else:
                self.index = 0

        self.easy = self.text

    def __str__(self):
        return 'Status Custom Column Value'

    def __repr__(self):
        return 'StatusValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def change_value(self, text=False, index=False, keep_original=False):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        if text and not index:
            self.repair_object.adjusted_values[self.id] = {'label': text}
            return {self.id: {'label': text}}
        elif index and not text:
            self.repair_object.adjusted_values[self.id] = {'index': index}
            return {self.id: {'index': index}}
        else:
            raise exceptions.ColumnInput(self.repair_object.name, self.attribute)


class TextValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if isinstance(column_value, str):
            self.text = None
        else:
            self.text = column_value.text

        self.easy = self.text

    def __str__(self):
        return 'Text Custom Column Value'

    def __repr__(self):
        return 'TextValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def change_value(self, text):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        self.repair_object.adjusted_values[self.id] = text
        return {self.id: text}


class HourValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if isinstance(column_value, str):
            self.hour = None
            self.minute = None
        else:
            self.hour = column_value.hour
            self.minute = column_value.minute

        if self.hour:
            self.easy = '{}:{}'.format(self.hour, self.minute)
        else:
            self.easy = None

    def __str__(self):
        return 'Hour Custom Column Value'

    def __repr__(self):
        return 'HourValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def change_value(self, hour_minute: list):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        self.repair_object.adjusted_values[self.id] = {'hour': hour_minute[0], 'minute': hour_minute[1]}
        return {self.id: {'hour': hour_minute[0], 'minute': hour_minute[1]}}


class ReadOnlyValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if isinstance(column_value, str):
            self.text = None
        elif column_value.text:
            self.text = column_value.text
        else:
            self.text = 0

        self.easy = self.text

    def __str__(self):
        return 'Text Custom Column Value'

    def __repr__(self):
        return 'TextValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )


class NumberValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if isinstance(column_value, str):
            self.number = 0
            self.text = None
        else:
            try:
                self.number = column_value.number
                self.text = str(column_value.number)
            except ValueError:
                num = getattr(column_value, 'value')
                self.number = float(num.replace('"', ''))
                self.text = str(self.number)

        if self.number is None:
            self.number = 0
            self.text = str(0)

        self.easy = self.number

    def __str__(self):
        return 'Number Custom Column Value'

    def __repr__(self):
        return 'NumberValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def change_value(self, number):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        self.repair_object.adjusted_values[self.id] = number
        return {self.id: number}


class DropdownValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)
        if self.moncli_val:
            ids_raw = json.loads(self.moncli_val.value)
            if ids_raw and self.moncli_val.text:
                self.ids = ids_raw['ids']
                self.labels = [label.strip() for label in self.moncli_val.text.split(',')]
            else:
                self.ids = []
                self.labels = []
        else:
            self.ids = []
            self.labels = []

        self.easy = self.labels

    def __str__(self):
        return 'Dropdown Custom Column Value'

    def __repr__(self):
        return 'DropdownValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

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
            print(labels_list)
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

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        self.date = None
        self.time = None
        self.text = None
        self.easy = None

        if self.moncli_val:
            values_raw = json.loads(self.moncli_val.value)
            if values_raw and self.moncli_val.text:
                self.date = values_raw['date']
                if 'time' in values_raw.keys():
                    self.time = values_raw['time']
                self.text = self.moncli_val.text

                self.easy = self.date

    def __str__(self):
        return 'Date Custom Column Value'

    def __repr__(self):
        return 'DateValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def change_value(self, date=None, time=None):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""

        if date and time:
            result = {self.id: {'date': date, 'time': time}}
        elif date and not time:
            result = {self.id: {'date': date, 'time': self.time}}
        elif time and not date:
            result = {self.id: {'date': self.date, 'time': time}}
        else:
            result = None
            print('DateValue change_value else route')

        self.repair_object.adjusted_values[self.id] = {'date': result[self.id]['date'], 'time': result[self.id]['time']}
        return result


class CheckboxValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if self.moncli_val:
            if self.moncli_val.text:
                self.checked = True
            else:
                self.checked = False
        else:
            self.checked = False

        self.easy = self.checked

    def __repr__(self):
        return 'CheckBoxValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def __str__(self):
        return 'Checkbox Custom Column Value'

    def change_value(self, checked=False):
        """Changes this column value and adds it to the 'adjusted_columns' attribute of repair
        keep_original allows the creation of a new value while maintaining the original object
        but may not work in some cases"""
        if checked:
            self.repair_object.adjusted_values[self.id] = {'checked': 'true'}
            return {self.id: {'checked': 'true'}}
        else:
            self.repair_object.adjusted_values[self.id] = {}
            return {self.id: {}}


class LinkValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if self.moncli_val:
            values_raw = json.loads(self.moncli_val.value)
            if values_raw:
                self.url = values_raw['url']
                self.text = values_raw['text']
            else:
                self.url = None
                self.text = None

        else:
            self.url = None
            self.text = None

        self.easy = self.text

    def change_value(self, text_url: list):
        """Will change the value for a Link column, however the url for this column is currently
        set to https://icorrect.zendesk.com/{TICKET NUMBER}, so will only work for the Ticket Column"""

        text = str(text_url[0])
        url = str(text_url[1])
        self.repair_object.adjusted_values[self.id] = {
            'url': url,
            'text': text
        }
        return {
            self.id: {
                'url': url,
                'text': text
            }
        }

    def __str__(self):
        return 'URL Link Custom Column Value'

    def __repr__(self):
        return 'LinkValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )


class ConnectValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if isinstance(column_value, str):
            self.id = None
        else:
            convert = json.loads(column_value.value)
            if convert:
                self.id = convert['linkedPulseIds'][0]['linkedPulseId']
            else:
                self.id = None

        self.easy = self.id

    def __str__(self):
        return 'Connect Boards Custom Column Value'

    def __repr__(self):
        return 'LinkValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def change_value(self, text=False, index=False, keep_original=False):
        """Currently Not Able to complete this function"""
        raise exceptions.NotDevelopedError('Connect Boards')


class SubitemValue(ColumnWrapper):

    def __init__(self, repair_object, attribute, column_value):
        super().__init__(repair_object, attribute, column_value)

        if isinstance(column_value, str):
            self.ids = None

        else:
            convert = json.loads(column_value.value)
            if convert:
                self.ids = [item['linkedPulseId'] for item in convert['linkedPulseIds']]
            else:
                self.ids = []

        self.easy = self.ids

    def __str__(self):
        return 'Subitem Custom Column Value'

    def __repr__(self):
        return 'SubitemValue(ID: {}, attribute: {}, column_val: {})'.format(
            self.repair_object.id,
            self.attribute,
            self.moncli_val
        )

    def delete_all_subitems(self):
        client = manage.Manager().create_client()
        if self.ids:
            for m_id in self.ids:
                for result in client.get_items(ids=[m_id], limit=1):
                    result.delete()
