from pprint import pprint as p

from icv5.components.monday.boardItems_misc import StuartDataItem
from icv5.components.monday import boardItems_main
from icv5.components.stuart import stuart


test = boardItems_main.MainBoardItem(1002886137)

test.booking_date.change_value(date='2025-12-25', time='13:00:00')
test.apply_column_changes()