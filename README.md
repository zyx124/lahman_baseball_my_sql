# lahman_baseball_my_sql

This is a lahman baseball database using python and MySQL.

The original data is in the compressed sql file.

Deployed on REST API, the queries can be implemented in browser or other test tools like Postman.

After running ```aeneid.py```, the following types of queries can be done:

1. GET:
  - /api<dbname>/<table_name>/<primary_key_value>?fields=f1, f2, f3
  - /api<dbname>/<table_name>q=<some_query_string>
  - /api<dbname>/<table_name>/<primary_key>/<table2_name>?query_string
2. DELETE and PUT
  - /api/<dbname>/<table_name>/<primary_key>
3. POST
  - /api/<dbname>/<table_name>
  - /api/<dbname>/<table_name>/<primary_key>/table_name
  
Some of the test files are located in /aeneid/test.

Foundamental structure has completed but some errors need to be modified.

---
The CSVDataTable is the file to directly manipulate data from .csv files. It can realize #insert, find_by_template, delete, import, save, load# and #JOIN# functions.
