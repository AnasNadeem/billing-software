## How to run this software

### Prequisite
* You should have Python and Postgresql installed on your Machine.
Now Open Terminal or Shell.

### Steps:
1. ```python3 -m venv env```
2. If on mac or linux: ```source env/bin/activate```. Windows: ```.\env\scripts\activate```
3. ``` python -m pip install requirements.txt ```
4. Open postgresql ```CREATE DATABASE mobiledb;```
5. Update DB_PASS and others in constants.py with your DATABASE PASSWORD.
6. Now in terminal, run ```py  connect_database.py```
Database with Tables are now created.
7. Comment the Table queries in connect_database.py and comment out the ```INSERT INTO users (username, pass) VALUES (%s,%s)""", ("anas", "anas")```. 
8. Everything's DONE. Now play around  ```py  login_dash.py```


### ENJOY :)