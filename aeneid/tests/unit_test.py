from aeneid.dbservices.RDBDataTable import RDBDataTable
import logging
logging.basicConfig(level=logging.DEBUG)
from aeneid.dbservices import dataservice as ds


def test_create():

    tbl = RDBDataTable('People')
    print('test create: tbl = ', tbl)

def create_people():
    result = ds.create('lahman2017.people',{'playerID':  'yz3400', 'nameLast': 'Zhao', 'nameFirst': 'Yuxin', 'birthCountry':'CHN'})
    print('create_people returned: ', result)

def delete_people():
    result = ds.delete('lahman2017.people',['yz3400'])
    print('delete_people returned: ', result)



#create_people()
#test_create()
#delete_people()