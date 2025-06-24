# DB Migration
- Makesure you install flask-migrate 
```
pip install flask-migrate
```
- Exporting Flask App file so that it will be used by db
```bash
export FLASK_APP=app.py
```

- First Initialize the DB migration, The below command will create folder structure
```py
flask db init
```
- Whenever you create or modify models, generate a migration script that captures those changes:

```py
flask db migrate -m "Initial migration"
```

- The below command will apply the script against db
```py
flask db upgrade
```