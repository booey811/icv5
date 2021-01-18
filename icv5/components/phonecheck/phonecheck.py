# import os
# from urllib import parse
# from io import BytesIO
# import json
#
# from icv5.components.monday import manage
# import pycurl
#
#
# class PhoneCheckResult:
#     # Missing From Phone Check
#     # [Charging Port, Wireless]
#
#     # Columns to be auto-filled: Charging Port
#
#     standard_checks = {
#         'Bluetooth': 'wifi',  # Bluetooth Column
#         'Ear Speaker': 'charging_port4',  # Earpiece & Mesh Column
#         'Flashlight': None,  # HAS NO Column
#         'Flip Switch': 'charging_port8',  # Mute/Vol Buttons Column
#         'Front Camera': 'rear_camera',  # Front Camera Column
#         'Front Microphone': 'rear_lens',  # Siri Column
#         'Front Video Camera': 'rear_camera',  # Front Camera Column
#         'Front Camera Quality': 'rear_camera',  # Front Camera Column
#         'Loud Speaker': 'power_button',  # Loudspeaker Column
#         'Microphone': 'rear_housing',  # Microphone Column
#         'Network Connectivity': None,  # HAS NO Column
#         'Power Button': 'charging_port',  # Power Button Column
#         'Proximity Sensor': 'rear_camera',  # Front Camera Column
#         'Rear Camera': 'bluetooth',  # Rear Camera Column
#         'Rear Camera Quality': 'bluetooth',  # Rear Camera Column
#         'Rear Video Camera': 'bluetooth',  # Rear Camera Column
#         'Telephoto Camera': 'bluetooth',  # Rear Camera Column
#         'Telephoto Camera Quality': 'bluetooth',  # Rear Camera Column
#         'Vibration': 'siri',  # Haptic Column
#         'Video Microphone': 'charging_port',  # Power Button Column
#         'Volume Down Button': 'charging_port8',  # Mute/Volume Column
#         'Volume Up Button': 'charging_port8',  # Mute/Volume Column
#         'Wifi': 'power_button9',  # Wifi Column
#         'Face ID': 'front_screen5',  # Face ID Check Column
#         'Glass Cracked': 'status_1',  # Front Screen Column
#         'LCD': 'status_1',  # Front Screen Column
#         'NFC': 'haptic3'  # NFC Column
#     }
#
#     def __init__(self, imei):
#
#         self.refurb_id = None
#         self.check_info = None
#         self.cli_client = manage.Manager().create_client()
#
#         self.imei = imei
#
#     def get_device_info(self):
#
#         dictionary = {
#             'Apikey': os.environ['PHONECHECK'],
#             'Username': 'icorrect1',
#             'IMEI': self.imei
#         }
#
#         form = parse.urlencode(dictionary)
#         bytes_obj = BytesIO()
#         crl = pycurl.Curl()
#         crl.setopt(crl.URL, 'https://clientapiv2.phonecheck.com/cloud/cloudDB/GetDeviceInfo')
#         crl.setopt(crl.WRITEDATA, bytes_obj)
#         crl.setopt(crl.POSTFIELDS, form)
#         crl.perform()
#         crl.close()
#         response = bytes_obj.getvalue()
#         check_data_raw = response.decode('utf8')
#         check_info = json.loads(check_data_raw)
#         if check_info:
#             self.check_info = check_info
#             return check_info
#         else:
#             return False
#
#     def convert_check_info(self, check_info):
#         code_to_apply = self.get_next_code()
#         col_vals = {
#             'numbers17': int(check_info['BatteryHealthPercentage']),
#             'text84': code_to_apply
#         }
#         self.batt_percentage = int(check_info['BatteryHealthPercentage'])
#         if self.batt_percentage < 84:
#             col_vals['haptic2'] = {'index': 2}
#         else:
#             col_vals['haptic2'] = {'index': 3}
#
#         all_checks = []
#         ignore = ['Face ID', 'LCD', 'Glass Cracked']
#
#         for fault in check_info['Failed'].split(','):
#             all_checks.append([fault, 'Failed'])
#             if fault in ignore:
#                 continue
#             if fault in self.standard_checks and self.standard_checks[fault]:
#                 col_vals[self.standard_checks[fault]] = {'index': 2}
#
#         for passed in check_info['Passed'].split(','):
#             all_checks.append([passed, 'Passed'])
#             if passed in ignore:
#                 continue
#
#             if (passed in self.standard_checks) \
#                     and (self.standard_checks[passed]) \
#                     and (self.standard_checks[passed] not in col_vals):
#                 col_vals[self.standard_checks[passed]] = {'index': 3}
#
#         return [all_checks, col_vals]
#
#     def record_check_info(self):
#
#         info = self.get_device_info()
#
#         if not info:
#             manager.add_update(
#                 self.refurb_id,
#                 'error',
#                 status=[
#                     'status_14',
#                     'Unable to Fetch'
#                 ],
#                 notify=[
#                     'Unable to Find this IMEI on Phonecheck',
#                     self.user_id
#                 ]
#             )
#             return False
#         add_to_board = self.convert_check_info(info)
#         add_to_board[1]['status_14'] = {'label': 'Complete'}
#         for item in add_to_board[1]:
#             value = {item: add_to_board[1][item]}
#             print(value)
#             self.refurb_item.change_multiple_column_values(value)
#         update = [str(item[0]) + ': ' + str(item[1]) for item in add_to_board[0]]
#         self.refurb_item.add_update("\n".join(update))
#
#     def get_next_code(self):
#
#         for pulse in monday_client.get_items(ids=[906832350], limit=1):
#             item = pulse
#
#         code = item.get_column_value(id='text0').text
#         letter = code.split('-')[0]
#         number = code.split('-')[1]
#         new_code = str(letter) + str(int(number) + 1)
#         replace_code = str(letter) + '-' + str(int(number) + 1)
#         item.change_multiple_column_values({
#             'text0': replace_code
#         })
#         return new_code
