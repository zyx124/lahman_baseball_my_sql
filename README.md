# lahman_baseball_my_sql

![Structure](https://github.com/zyx124/lahman_baseball_my_sql/blob/master/pasted%20image%200.png)

This is a lahman baseball database using python and MySQL.

The original data is in the compressed sql file.

The database model EER diagram is shown below.

![EER diagram of database model](https://github.com/zyx124/lahman_baseball_my_sql/blob/master/eer_diagram.png)

The REST API is deployed by python (3.5.2) and Flask (1.0.2), the queries can be implemented in browser or other test tools like Postman.

After running ```aeneid.py``` in /Flask_REST/, the following types of queries can be done:

1. GET:
- /explain/<concept>

  - /api<dbname>/<table_name>/<primary_key_value>?fields=f1, f2, f3
  - /api<dbname>/<table_name>q=<some_query_string>
  - /api<dbname>/<table_name>/<primary_key>/<table2_name>?query_string
2. DELETE and PUT
  - /api<dbname>/<table_name>/<primary_key>
3. POST
  - /api<dbname>/<table_name>
  - /api<dbname>/<table_name>/<primary_key>/table_name

Some of the test files are located in /Flask_REST/aeneid/test.

Fundamental structure has completed but some errors need to be modified.

---
2019.5

Some graph database implementation is added in the ```nosql``` folder.

---
2019.7

The CSVDataTable is the file to directly manipulate data from .csv files. It can realize ```insert```, ```find_by_template```, ```delete```, ```import```, ```save```, ```load``` and ```JOIN``` functions.