from pprint import pprint as p
import time
import os

from moncli.entities import create_column_value
from moncli import ColumnType
import settings
from zenpy.lib.api_objects import CustomField

from icv5.components.monday.boardItems_misc import StuartDataItem

from icv5.components.monday import boardItems_main, boardItems_inventory, boardItems_reporting, manage, boardItems_financial, boardItems_misc
from icv5.components.stuart import stuart
from icv5.components.zendesk import ticket
from icv5.components.zendesk.assets import custom_fields

from pprint import pprint as p

webhook = {'event': {'userId': 4251271}}

item_id = 1092341311

main_item = boardItems_main.MainBoardItem(item_id=item_id, webhook_payload=webhook)

courier = stuart.StuartClient(main_item=main_item)

try:
    job_payload = courier.validate_job_details('delivery')
    courier.book_courier_job(job_payload)
except (stuart.DistanceTooGreat or stuart.EmailInvalid or stuart.CannotGeocodeAddress or
        stuart.UnknownValidationError or stuart.CourierDetailsMissing or stuart.PhoneNumberInvalid):
    pass