from flask import Flask  # Importing Flask Module
from flask_sqlalchemy import SQLAlchemy #Import Flask SQL Alchemy for MYSQL ORM
import datetime # For Date time formatting
from flask_migrate import Migrate # For database migration


app = Flask(__name__) #Initializing the flask. When a Python file is imported as a module, __name__ is set to the module's name (i.e., the filename without .py

# SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/url_shortner" #setting connection url for the DB.

db = SQLAlchemy(app) # Connecting App with DB

# Creating Table Schema
class Links(db.Model):
    #Defining Table name
    __tablename__ = 'url_shortner'
    
    # Defining Table Schema
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_url = db.Column(db.String(18), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow)

    # The __repr__ method defines how your object is represented as a string, mainly for debugging and logging.
    def __repr__(self):
        return f'<Link {self.short_url} -> {self.original_url}>'
    
# Here we are initializing DB Migration
migrate = Migrate(app, db)