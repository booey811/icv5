import os
import json
import requests
from pprint import pprint as p
import datetime

import pycurl
from io import BytesIO

import settings
from icv5.components.monday import manage, boardItems_misc
from icv5.components.zendesk import ticket


class StuartClient:

    def __init__(self, main_item=None):
        self.main_item = main_item

        if os.environ['STUARTPROD'] == 'True':
            self.production = True
        else:
            self.production = False

        self.token = None

    @staticmethod
    def check_data_presence_and_create_address_string(mainboard_item):

        attributes_strict = ['name', 'phone', 'email', 'address1', 'postcode']
        attributes_optional = ['address2', 'company']

        attributes_dict = {}
        comment = None

        for data in attributes_optional + attributes_strict:
            try:
                value = getattr(mainboard_item, data).easy
            except AttributeError:
                value = getattr(mainboard_item, data)
            if value:
                attributes_dict[data] = value
            else:
                attributes_dict[data] = None

        for detail in attributes_dict:
            if detail in attributes_strict and not attributes_dict[detail]:
                raise CourierDetailsMissing(mainboard_item, detail)
            elif detail == 'address2' and attributes_dict[detail]:
                comment = attributes_dict[detail]

        add_string = '{} {} London'.format(attributes_dict['address1'], attributes_dict['postcode'])

        return {
            'address': add_string,
            'comment': comment,
            'firstname': attributes_dict['name'].split()[0],
            'lastname': attributes_dict['name'].split()[1],
            'email': attributes_dict['email'],
            'phone': attributes_dict['phone'],
            'company': attributes_dict['company']
        }

    def create_job_payload(self, direction):

        client_details = self.check_data_presence_and_create_address_string(self.main_item)

        icorrect_address = {
            'address': 'iCorrect 12 Margaret Street W1W 8JQ London',  # Required
            'comment': '',
            'contact': {
                'firstname': 'Gabriel',  # Required
                'lastname': 'Barr',  # Required
                'phone': '02070998517',  # Required
                'email': 'support@icorrect.co.uk',  # Required
                'company': 'iCorrect'
            }
        }

        client_address = {
            'address': client_details['address'],  # Required
            'contact': {
                'firstname': client_details['firstname'],  # Required
                'lastname': client_details['lastname'],  # Required
                'phone': client_details['phone'],  # Required
                'email': client_details['email'],  # Required
                'company': None
            }
        }

        if client_details['company']:
            client_address['contact']['company'] = client_details['company']
        if client_details['comment']:
            client_address['comment'] = client_details['comment']

        payload = {
            'job': {
                'assignment_code': self.generate_assignment_code(direction),  # Will Need to Be Generated
                'pickups': [],
                'dropoffs': []
            }
        }

        if direction == 'collection':
            payload['job']['pickups'].append(client_address)
            payload['job']['dropoffs'].append(icorrect_address)
            date_time = self.set_collection_datetime()
            if date_time:
                print('future booking')
                payload['job']['pickup_at'] = date_time
        elif direction == 'delivery':
            payload['job']['pickups'].append(icorrect_address)
            payload['job']['dropoffs'].append(client_address)

        payload['job']['dropoffs'][0]['package_type'] = 'small'

        return payload

    def set_collection_datetime(self):
        main_time = self.main_item.booking_date.time
        main_date = self.main_item.booking_date.date
        if not main_time or not main_date:
            return False
        formatted = '{}T{}'.format(main_date, main_time)
        return formatted

    def generate_assignment_code(self, direction):
        item_id = self.main_item.id
        if direction == 'collection':
            direct = 'COL'
        else:
            direct = 'RTN'
        time = '{}{}'.format(str(datetime.datetime.now().hour), str(datetime.datetime.now().minute))

        return '{} {} {}'.format(item_id, direct, time)

    def authenticate(self):
        if self.production:
            url = "https://api.stuart.com/oauth/token"
            payload = "client_id={}&client_secret={}&scope=api&grant_type=client_credentials".format(
                os.environ["STUARTID"], os.environ["STUARTSECRET"])
            headers = {'content-type': 'application/x-www-form-urlencoded'}
        else:
            payload = {
                "scope": "api",
                "grant_type": "client_credentials",
                "client_id": os.environ["STUARTIDSAND"],
                "client_secret": os.environ["STUARTSECRETSAND"]
            }
            url = "https://api.sandbox.stuart.com/oauth/token"
            payload = json.dumps(payload)
            headers = {'content-type': "application/json"}
        response = requests.request('POST', url, data=payload, headers=headers)
        info = json.loads(response.text)
        self.token = info["access_token"]

    def validate_job_details(self, direction):
        if not self.token:
            self.authenticate()
        if self.production:
            url = 'https://api.stuart.com/v2/jobs/validate'
        else:
            url = 'https://api.sandbox.stuart.com/v2/jobs/validate'
        job_payload = self.create_job_payload(direction)
        payload = json.dumps(job_payload)
        headers = {
            'content-type': "application/json",
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = requests.request('POST', url=url, data=payload, headers=headers)
        try:
            self.process_job_validation_response(response)
            return job_payload
        except CannotGeocodeAddress or EmailInvalid or PhoneNumberInvalid:
            print('Exception Raised')
            return False

    def process_job_validation_response(self, response):
        response_info = json.loads(response.text)
        if response.status_code == 200:
            return True
        elif response_info['error'] == 'CANT_GEOCODE_ADDRESS':
            raise CannotGeocodeAddress(self.main_item)
        elif response_info['error'] == 'EMAIL_INVALID':
            raise EmailInvalid(self.main_item, self.main_item.email)
        elif response_info['error'] == 'PHONE_INVALID':
            raise PhoneNumberInvalid(self.main_item, self.main_item.phone)
        elif response_info['error'] == 'JOB_DISTANCE_NOT_ALLOWED':
            raise DistanceTooGreat(self.main_item)
        else:
            raise UnknownValidationError(self.main_item, response)

    def book_courier_job(self, job_payload):
        if not self.token:
            self.authenticate()
        if self.production:
            url = 'https://api.stuart.com/v2/jobs'
        else:
            url = 'https://api.sandbox.stuart.com/v2/jobs'

        payload = json.dumps(job_payload)
        headers = {
            'content-type': "application/json",
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = requests.request('POST', url=url, data=payload, headers=headers)
        self.process_successful_booking(response)

    def process_successful_booking(self, response):

        res_dict = json.loads(response.text)
        new = boardItems_misc.StuartDataItem(blank_item=True)

        if response.status_code == 201:
            info = {
                'assignment_code': res_dict['assignment_code'],
                'delivery_postcode': res_dict['deliveries'][0]['dropoff']['address']['postcode'],
                'delivery_address': res_dict['deliveries'][0]['dropoff']['address']['street'],
                'dropoff_id': res_dict['deliveries'][0]['dropoff']['id'],
                'delivery_id': res_dict['deliveries'][0]['id'],
                'collection_postcode': res_dict['deliveries'][0]['pickup']['address']['postcode'],
                'collection_address': res_dict['deliveries'][0]['pickup']['address']['street'],
                'pickup_id': res_dict['deliveries'][0]['pickup']['id'],
                'tracking_url': res_dict['deliveries'][0]['tracking_url'],
                'distance': res_dict['distance'],
                'stuart_id': res_dict['id'],
                'cost_ex': res_dict['pricing']['price_tax_excluded'],
                'tax': res_dict['pricing']['tax_amount'],
                'estimated_time': res_dict['duration']
            }

            if info['delivery_postcode'] == 'W1W 8JQ':
                name = '{} COLLECTION'.format(self.main_item.name.replace('"', '').replace("'", ''))
                self.main_item.be_courier_collection.change_value('Booking Complete')
                if self.main_item.booking_date.time:
                    new.booking_time.change_value(
                        [int(self.main_item.booking_date.time.split(':')[0]),
                         int(self.main_item.booking_date.time.split(':')[1])]
                    )
                else:
                    new.booking_time.change_value([int(datetime.datetime.now().hour), int(datetime.datetime.now().minute)])

            else:
                name = '{} RETURN'.format(self.main_item.name.replace('"', '').replace("'", ''))
                self.main_item.be_courier_return.change_value('Booking Complete')
                new.booking_time.change_value([int(datetime.datetime.now().hour), int(datetime.datetime.now().minute)])

            new.change_multiple_attributes(
                [
                    ['assignment_code', str(info['assignment_code']).replace('"', '').replace("'", '')],
                    ['stuart_job_id', str(info['stuart_id']).replace('"', '').replace("'", '')],
                    ['ex_vat', round(float(info['cost_ex']), 2)],
                    ['vat', round(float(info['tax']), 2)],
                    ['delivery_postcode', str(info['delivery_postcode']).replace('"', '').replace("'", '')],
                    ['collection_postcode', str(info['collection_postcode']).replace('"', '').replace("'", '')],
                    ['tracking_url', [str('Tracking').replace('"', '').replace("'", ''), str(info['tracking_url']).replace('"', '').replace("'", '')]],
                    ['estimated_time', int(res_dict['duration'])],
                    ['distance', round(float(info['distance']), 2)],
                    ['status', 'In Progress']
                ],
                return_only=True
            )

            stuart_log = manage.Manager().get_board('stuart_data_new').add_item(
                item_name=name,
                column_values=new.adjusted_values
            )

            update = ['{}: {}'.format(item, str(info[item]).replace('"', '').replace("'", '')) for item in info]

            self.add_tracking_to_zendesk(update, info['tracking_url'])

            body = '\n'.join(update)
            body = body.replace('"', '').replace("'", '')

            self.main_item.item.add_update(body)

            self.main_item.apply_column_changes()

    def add_tracking_to_zendesk(self, update, tracking_url):
        if not self.main_item.zendesk_id.easy:
            update.append('\n\nTHERE IS NO ZENDESK TICKET ASSOCIATED WITH THIS REPAIR - NO TRACKING LINK HAS BEEN SENT TO THE CUSTOMER')
        else:
            zendesk = ticket.ZendeskTicket(str(self.main_item.zendesk_id.easy))
            zendesk.tracking_url.adjust_value(tracking_url)
            zendesk.client.tickets.update(zendesk.ticket)


class PhoneNumberInvalid(Exception):
    def __init__(self, main_item, phone_number):
        print('The Phone Number you have provided ({}) is not valid. Please check and try again'.format(phone_number))
        manage.Manager().add_update(
            main_item,
            client_account='error',
            update='Unable to Book Courier Job for {}. The Phone Number you have provided ({}) is not valid.'.format(
                main_item.name,
                phone_number
            ),
            notify=[
                'Unable to Book Courier Job for {}. The Phone Number you have provided ({}) is not valid.'.format(
                    main_item.name,
                    phone_number
                ),
                main_item.user_id
            ]
        )
        main_item.status.change_value('Error')
        main_item.be_courier_collection.change_value('Booking Failed')
        main_item.apply_column_changes()


class EmailInvalid(Exception):
    def __init__(self, main_item, email):
        print('The email you have provided ({}) is not valid. Please check and try again'.format(email))
        manage.Manager().add_update(
            main_item,
            client_account='error',
            update='Unable to Book Courier Job for {}. The email you have provided ({}) is not valid.'.format(
                main_item.name,
                email
            ),
            notify=[
                'Unable to Book Courier Job for {}. The email you have provided ({}) is not valid.'.format(
                    main_item.name,
                    email
                ),
                main_item.user_id
            ]
        )
        main_item.status.change_value('Error')
        main_item.be_courier_collection.change_value('Booking Failed')
        main_item.apply_column_changes()


class CannotGeocodeAddress(Exception):
    def __init__(self, main_item):
        print(
            """The address you have provided ({} {}) is not accurate enough.
            Please check and try again or book the courier manually""".format(
                main_item.address1.easy,
                main_item.postcode.easy
            ))
        manage.Manager().add_update(
            main_item,
            client_account='error',
            update="""The address you have provided ({} {}) is not accurate enough.
                Please check and try again or book the courier manually""".format(
                main_item.address1.easy,
                main_item.postcode.easy
            ),
            notify=[
                """The address you have provided ({} {}) is not accurate enough.
                Please check and try again or book the courier manually""".format(
                    main_item.address1.easy,
                    main_item.postcode.easy
                ),
                main_item.user_id
            ]
        )
        main_item.status.change_value('Error')
        main_item.be_courier_collection.change_value('Booking Failed')
        main_item.apply_column_changes()


class CourierDetailsMissing(Exception):
    attribute_translate = {
        'address1': 'Street Address',
        'phone': 'Phone Number',
        'email': 'Email',
        'postcode': 'Post Code'
    }

    def __init__(self, main_item, attribute):
        print('Unable to Book Courier Job for {}. Please ensure the {} column is filled in correctly'.format(
            main_item.name,
            self.attribute_translate[attribute])
        )
        manage.Manager().add_update(
            main_item,
            client_account='error',
            update='Unable to Book Courier Job for {}. Please ensure the {} column is filled in correctly'.format(
                main_item.name,
                self.attribute_translate[attribute]
            ),
            notify=[
                'Unable to Book Courier Job for {}. Please ensure the {} column is filled in correctly'.format(
                    main_item.name,
                    self.attribute_translate[attribute]
                ),
                main_item.user_id
            ]
        )
        main_item.status.change_value('Error')
        main_item.be_courier_collection.change_value('Booking Failed')
        main_item.apply_column_changes()


class DistanceTooGreat(Exception):

    def __init__(self, main_item):
        print('Unable to Book Courier Job for {}. The distance is too great, so please book through another method'.format(
            main_item.name
        ))
        manage.Manager().add_update(
            main_item,
            client_account='error',
            update='Unable to Book Courier Job for {}. The distance is too great, so please book through another method'.format(
                main_item.name,
            ),
            notify=[
                'Unable to Book Courier Job for {}. The distance is too great, so please book through another method'.format(
                    main_item.name,
                ),
                main_item.user_id
            ]
        )
        main_item.status.change_value('Error')
        main_item.be_courier_collection.change_value('Booking Failed')
        main_item.apply_column_changes()


class UnknownValidationError(Exception):
    def __init__(self, main_item, response):
        print('During Job Validation with Stuart an Unknown Error Has Occurred')
        print(response.text)
        manage.Manager().add_update(
            main_item,
            client_account='error',
            update='During Job Validation with Stuart for {} an Unknown Error Has Occurred\n\n{}\n{}'.format(
                main_item.name,
                response,
                response.text.replace('"', '')
            ),
            notify=[
                'During Job Validation with Stuart for {} an Unknown Error Has Occurred'.format(
                    main_item.name,
                ),
                4251271
            ]
        )
        main_item.status.change_value('Error')
        main_item.be_courier_collection.change_value('Booking Failed')
        main_item.apply_column_changes()
