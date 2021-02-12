from pprint import pprint as p
import time

from moncli.entities import create_column_value
from moncli import ColumnType

from icv5.components.monday.boardItems_misc import StuartDataItem
from icv5.components.monday import boardItems_main, boardItems_inventory, manage, boardItems_reporting
from icv5.components.stuart import stuart

finance = boardItems_reporting.FinancialItem(item_id=1048897492)
finance.void_entry()