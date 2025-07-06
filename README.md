# TODO

# DB Migration
- For Flask Migration to happen we need following modules to be installed. All these are covered in requireemnt.txt file. when you install from requirement.txt all below package will get installed automatically. Just covering here for knowledge purpose
    - flask_migrate - used for migration
    - pymysql - PythonMysql diaclet
    - cryptograpy - when mysql and mysqlclient or pymysql these uses Sha256 password and needs cryptography package to handle it.
# DB Migration command
- Migration initialization. This creates migration directory and other related things
```python
flask db init
```
- Create Migration locally. The below command will create new migration file. This file will contains all our DB schema changes and flask sql will also version each file getting generated. 
```python
flask db migrate -m "Initial commit"
```
- Applying the changes to DB. This below command will apply the migrateion files to DB
```python
flask db upgrade
```


## DB Connections
- Create Model for DB
- Establish Connection with db
- Migrate the model to db
- Verify the same
- Create a function to add entry to db
- Create a function get a specific full url as ouptut by passing short url as input
# Input

curl -X POST http://localhost:5000/short -H "Content-Type: application/json" -d '{"original_url": "https://example.com"}'

curl -X GET http://localhost:5000/LJ6zAP -H "Content-Type: application/json" 