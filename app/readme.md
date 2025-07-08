# URL Shortner
# DB
- We are using MYSQL Db. For local setup make sure you have docker up and running and run the following command to spinup Mysql db container on your docker
```bash
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 mysql
```
- The username and password for the db is: 
    - `username`: `root` and `password`: `password`


## DB Migration
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



curl -X POST http://localhost:5000/short -H "Content-Type: application/json" -d '{"original_url": "https://google.com"}'

curl -X GET http://localhost:5000/LJ6zAP -H "Content-Type: application/json" 