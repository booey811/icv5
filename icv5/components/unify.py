from pprint import pprint as p
import time
import os

from moncli.entities import create_column_value
from moncli import ColumnType
import settings
from zenpy.lib.api_objects import CustomField

from icv5.components.monday.boardItems_misc import StuartDataItem

from icv5.components.monday import boardItems_main, boardItems_inventory, boardItems_reporting, manage, boardItems_financial
from icv5.components.stuart import stuart
from icv5.components.zendesk import ticket
from icv5.components.zendesk.assets import custom_fields

from pprint import pprint as p

webhook_payload = {'event': {'userId': 4251271}}

item_id = 1086301501

finance = boardItems_financial.FinancialBoardItem(item_id=item_id, webhook_payload=webhook_payload)
finance.disassemble_repairs_profile()