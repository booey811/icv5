from pprint import pprint as p
import time
import os

from moncli.entities import create_column_value
from moncli import ColumnType
import settings
from zenpy.lib.api_objects import CustomField

from icv5.components.monday.boardItems_misc import StuartDataItem

from icv5.components.monday import boardItems_main, boardItems_inventory, boardItems_reporting, manage
from icv5.components.stuart import stuart
from icv5.components.zendesk import ticket

from pprint import pprint as p

test = ticket.ZendeskTicket(8345)

for field in test.ticket.custom_fields:

    print(field)