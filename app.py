from flask import Flask  # Importing Flask Module
from db import db, Links
from utils.utils import * 
from flask_migrate import Migrate # For database migration
from flask import request, redirect, jsonify
import random, string

#Initializing the flask. When a Python file is imported as a module, __name__ is set to the module's name (i.e., the filename without .py
app = Flask(__name__) 
## SQLALCHEMY DB Config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/url_shortner" #setting connection url for the DB.
# Connects Flask App to the DB with the above configuration
db.init_app(app) 
# Here we are initializing DB Migration
migrate = Migrate(app, db)


@app.route('/short', methods=['POST'])
def create_short_url():
    data = request.get_json() # Get Request details
    original_url = data.get('original_url') # Extracting original url from data block of request
    # Validating original url exist in the request block else return error message
    if not original_url:
        return jsonify({"error": "Original Url Required"}), 422
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    check_exist = check_short_key(db.session, short_code)  # Pass db.session here
    
    add_to_db(db.session,original_url, short_code)
    short_url = request.host_url + short_code
    return jsonify({"short_code": short_url}), 201


@app.route('/<short_code>', methods=['GET'])
def redirect_to_original_url(short_code):
    get_url_data = check_short_key(db.session,short_code)
    if not get_url_data:
        return jsonify({"error": "Not Found"}), 404
    app.logger.debug(f"Lookup for {short_code}: {get_url_data.original_url}")
    return redirect(get_url_data.original_url, 302)


if __name__ == "__main__":
    app.run(debug=True)