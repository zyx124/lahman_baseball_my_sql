import sys
import json
import os

sys.path.append('/home/zyx/W4111_HW2/aeneid/dbservices')
from RDBDataTable import RDBDataTable

def test_find_by_primary_key():
    t = RDBDataTable('People', key_columns=['playerID'], connect_info=None, debug=False)

    x = t.find_by_primary_key(['willite01'], ['playerID', 'nameLast', 'nameFirst', 'throws', 'bats'])

    print('find_by_primary_key result = ',x)