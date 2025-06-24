from flask import Flask     # For overall flask operations
from flask_sqlalchemy import SQLAlchemy # To handle Database. SQLAlchemy is ORM for Python
from sqlalchemy import inspect  # To inpsect and read Content
from datetime import datetime   # For date time 
from flask_migrate import Migrate   # For database schema migration


app = Flask(__name__) # Here we are initializing Flask app and assign to a variable called app

#mysql = type of db, pymysql = Python driver used to connect to db and followed by url and /links is the db name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/links'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initializing Connection to the DB with above DB URI and assigning it to db
db = SQLAlchemy(app)

# Heee we are initializing DB Migration using sql app and db details. 
migrate = Migrate(app, db)

class Link(db.Model):
    __tablename__ = 'links' #Table name in the database

    # Here we are defining DB Schema, this is how we define Schema in SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_url = db.Column(db.String(18), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Simple initialization, Optional
    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url
        self.visits = 0
    
    # It defines how an instance of the class is represented as a string, mainly for debugging and logging.
    # When you print an object or inspect it in the console, Python calls __repr__ to get a meaningful string.
    def __repr__(self):
        return f'<Link {self.short_url} -> {self.original_url}>'


@app.route('/tables')
def list_tables():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return {'tables': tables}

if __name__ == '__main__':
    app.run(debug = True)

