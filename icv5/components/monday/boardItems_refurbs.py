from icv5.components.monday import boardItem, column_keys, manage, exceptions


class RefurbWrapper(boardItem.MondayWrapper):

    def __init__(self, item_id, parent_obj, blank_item=False):

        new_column_dictionary = column_keys.refurb_wrapper

        super().__init__()

        self.top_level = None
        self.purchasing = None
        self.received = None
        self.tested = None
        self.repairing = None
        self.selling = None
        self.final_stats = None
        self.returns = None
        self.backlog = None

        if not blank_item:
            self.set_client_and_item(self, item_id)

        column_dictionary = {**new_column_dictionary, **parent_obj.column_dictionary}
        for item in column_dictionary:
            setattr(self, item, None)
        self.set_attributes(self, column_dictionary)

        if blank_item:
            self.create_blank_item()

    def create_blank_item(self):

        return self

    @staticmethod
    def get_batch_unit_codes(code_type):

        results = manage.Manager().create_client().get_items(ids=[929334859], limit=1)
        if len(results) != 1:
            raise exceptions.NoItemsFoundFromMondayClientSearch(929334859)
        else:
            for pulse in results:
                code_pulse = pulse
                break

        if code_type == 'batch':
            column_id = 'batch_code'
        elif code_type == 'unit':
            column_id = 'unit_code'
        else:
            raise exceptions.IncorrectCodeTypeRequest(code_type)

        code = code_pulse.get_column_value(column_id).text

        return code.replace('-', '')


class RefurbTopLevelBoardItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_toplevel

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbPurchasingItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_purchasing

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbReceivedItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_received

    standard_checks = {
        'Bluetooth': 'wifi',  # Bluetooth Column
        'Ear Speaker': 'power_button',  # Earpiece & Mesh Column
        'Flashlight': None,  # HAS NO Column
        'Flip Switch': 'wireless',  # Mute/Vol Buttons Column
        'Front Camera': 'rear_lens',  # Front Camera Column
        'Front Microphone': 'front_camera',  # Siri Column
        'Front Video Camera': 'rear_lens',  # Front Camera Column
        'Front Camera Quality': 'rear_lens',  # Front Camera Column
        'Loud Speaker': 'earpiece_mesh',  # Loudspeaker Column
        'Microphone': 'rear_glass',  # Microphone Column
        'Network Connectivity': None,  # HAS NO Column
        'Power Button': 'mute_vol_buttons',  # Power Button Column
        'Proximity Sensor': 'rear_lens',  # Front Camera Column
        'Rear Camera': 'bluetooth',  # Rear Camera Column
        'Rear Camera Quality': 'bluetooth',  # Rear Camera Column
        'Rear Video Camera': 'bluetooth',  # Rear Camera Column
        'Telephoto Camera': 'bluetooth',  # Rear Camera Column
        'Telephoto Camera Quality': 'bluetooth',  # Rear Camera Column
        'Vibration': 'nfc',  # Haptic Column
        'Video Microphone': 'mute_vol_buttons',  # Power Button Column
        'Volume Down Button': 'wireless',  # Mute/Volume Column
        'Volume Up Button': 'wireless',  # Mute/Volume Column
        'Wifi': 'loudspeaker',  # Wifi Column
        'Face ID': 'status5',  # Face ID Check Column
        'Glass Cracked': 'battery',  # Front Screen Column
        'LCD': 'battery',  # Front Screen Column
        'NFC': 'siri'  # NFC Column
    }

    face_id_values = {
        'H/L': 'Higher/Lower',
        'Unable': 'Unable to Activate',
        'Other(FaceID)': 'Other',
        '_id': 'front_screen5'
    }

    screen_values = {
        'G': 'Glass Only',
        'G & T': 'Glass & Touch',
        'G T & L': 'Glass, Touch & LCD',
        '_id': 'status_1'
    }

    rear_values = {
        'RG': 'Rear Glass Required',
        'RH': 'Rear Housing Required',
        '_id': 'front_screen'
    }

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

    def process_phonecheck_results(self, phonecheck_object, test=False):
        check_info = phonecheck_object.get_device_info()
        new_unit_code = self.get_batch_unit_codes('unit')

        # Battery Percentage and Unit Code
        col_vals = {
            'numbers': int(check_info['BatteryHealthPercentage']),
            'unit_code': new_unit_code,
            'microphone': {'label': 'No Repair Required'},
            'charging_port': {'label': 'No Repair Required'}
        }

        # Battery Repair Required Column
        if int(check_info['BatteryHealthPercentage']) < 84:
            col_vals['face_id'] = {'label': 'Repair Required'}
        else:
            col_vals['face_id'] = {'label': 'No Repair Required'}

        all_checks = []
        ignore = ['Face ID', 'LCD', 'Glass Cracked', 'Digitizer']

        for fault in check_info['Failed'].split(','):
            all_checks.append([fault, 'Failed'])
            if fault in ignore:
                continue
            elif fault in self.standard_checks and self.standard_checks[fault]:
                getattr(self, self.standard_checks[fault]).change_value(index=2)
            else:
                print('Fault Not Translated to Monday: {}'.format(fault))

        for passed in check_info['Passed'].split(','):
            all_checks.append([passed, 'Passed'])
            if passed in ignore:
                continue
            if (passed in self.standard_checks) \
                    and (self.standard_checks[passed]) \
                    and (self.standard_checks[passed] not in col_vals):
                col_vals[self.standard_checks[passed]] = {'label': 'No Repair Required'}

        self.calibrate_screen_column(check_info, col_vals)
        self.calibrate_face_id_column(check_info, col_vals)
        self.calibrate_rear_glass_column(check_info, col_vals)


        self.item.change_multiple_column_values({'status': {'label': 'Complete'}})

        if test:
            for value in col_vals:
                print(value)
                print(col_vals[value])
                self.item.change_multiple_column_values({value: col_vals[value]})
        else:
            self.item.change_multiple_column_values(col_vals)


    def calibrate_rear_glass_column(self, check_info, col_vals):
        rear_values = {
            'RG': 'Rear Glass Required',
            'RH': 'Rear Housing Required',
            '_id': 'front_screen'
        }

        cosmetics = check_info['Cosmetics'].split(',')

        if 'RG' in cosmetics:
            col_vals['front_screen'] = {'label': 'Rear Glass Required'}
        elif 'RH' in cosmetics:
            col_vals['front_screen'] = {'label': 'Rear Housing Required'}
        else:
            col_vals['front_screen'] = {'label': 'No Repair Required'}

    def calibrate_face_id_column(self, check_info, col_vals):

        cosmetics = check_info['Cosmetics'].split(',')

        if 'status5' in col_vals:
            return
        elif 'Face ID' in check_info['Passed']:
            col_vals['status5'] = {'label': 'No Repair Required'}
        elif 'H/L' in cosmetics:
            col_vals['status5'] = {'label': 'Higher/Lower'}
        elif 'Unable' in cosmetics:
            col_vals['status5'] = {'label': 'Unable to Activate'}
        elif 'Other(FaceID)' in cosmetics:
            col_vals['status5'] = {'label': 'Other'}

    def calibrate_screen_column(self, check_info, col_vals):

        if 'LCD' in check_info['Failed']:
            col_vals['battery'] = {'label': 'Glass, Touch & LCD'}
        elif 'Digitizer' in check_info['Failed']:
            col_vals['battery'] = {'label': 'Glass & Touch'}
        elif 'Glass Cracked' in check_info['Failed']:
            col_vals['battery'] = {'label': 'Glass Only'}
        else:
            col_vals['battery'] = {'label': 'No Repair Required'}

    def add_to_tested_board(self):

        tested_item = RefurbTestedItem()

        attributes = [
            'imei_sn', 'batch_code', 'unit_code', 'face_id', 'battery', 'screen', 'rear_glass', 'microphone',
            'charging_port', 'wireless', 'mute_vol', 'power', 'earpiece', 'loudspeaker', 'bluetooth', 'rear_cam',
            'rear_lens', 'front_camera', 'siri', 'nfc'
        ]

        for attribute in attributes:
            pass


class RefurbTestedItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_tested

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbRepairingItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_repairing

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbSellingItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_selling

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbFinalItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_final

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbReturnItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_return

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)


class RefurbBacklogItem(RefurbWrapper):
    column_dictionary = column_keys.refurb_backlog

    def __init__(self, item_id=None, blank_item=None):
        if item_id:
            super().__init__(item_id, self)
        elif blank_item:
            super().__init__(None, self, blank_item=blank_item)

