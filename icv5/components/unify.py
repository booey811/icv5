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

stuuu = boardItems_misc.StuartDataItem.get_data_item(130609239)

test = boardItems_main.MainBoardItem(stuuu.assignment_code.easy.split()[0])

p(test.__dict__)