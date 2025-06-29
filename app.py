from flask import Flask     # For overall flask operations
from flask_sqlalchemy import SQLAlchemy # To handle Database. SQLAlchemy is ORM for Python
from sqlalchemy import inspect  # To inpsect and read Content
from datetime import datetime   # For date time 
from flask_migrate import Migrate   # For database schema migration
from flask import request, jsonify
import hashlib, base62
import datetime
import random


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
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Simple initialization, Optional
    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url
        self.visits = 0
    
    # It defines how an instance of the class is represented as a string, mainly for debugging and logging.
    # When you print an object or inspect it in the console, Python calls __repr__ to get a meaningful string.
    def __repr__(self):
        return f'<Link {self.short_url} -> {self.original_url}>'


@app.route('/shorten',methods=['POST'])
def create_short_url():
    data = request.get_json()
    original_url = data.get('original_url')
    if not original_url:
        return jsonify({"error":"Original Url required"}), 400
    
    base_url = f"{original_url}{datetime.datetime.now()}"
    encoded_url = base62.encode(hashlib.sha256(base_url.encode()).digest())
    print(encoded_url)
    shorterned_url = ''.join(random.choices(encoded_url, k=6))
    while Link.query.filter_by(short_url=shorterned_url).first() is not None:
        shorterned_url = ''.join(random.choices(encoded_url, k=6))

     # Step 4: Save new Link to DB
    new_link = Link(original_url=original_url, short_url=shorterned_url)
    db.session.add(new_link)
    db.session.commit()

    short_url = request.host_url + shorterned_url
    return jsonify({
        "message": "Short URL created",
        "short_url": short_url
    }), 201


if __name__ == '__main__':
    app.run(debug = True)

