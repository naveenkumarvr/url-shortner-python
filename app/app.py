from flask import Flask  # Importing Flask Module
from db import db, Links
from utils.utils import *
from utils.redis import *
from flask_migrate import Migrate # For database migration
from flask import request, redirect, jsonify
import random, string
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mysql_host = os.getenv("MYSQL_HOST", "localhost")

#Initializing the flask. When a Python file is imported as a module, __name__ is set to the module's name (i.e., the filename without .py
app = Flask(__name__) 
## SQLALCHEMY DB Config
app.config["SQLALCHEMY_DATABASE_URI"] = (f"mysql+pymysql://root:password@{mysql_host}:3306/url_shortner") #setting connection url for the DB.
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
    #Check Redis cache
    check_cache = check_redis_cache(short_code)
    if check_cache:
        return redirect(check_cache, 302)
    else:
        get_url_data = check_short_key(db.session,short_code)
        if not get_url_data:
            return jsonify({"error": "Not Found"}), 404
        app.logger.debug(f"Reading from database {short_code}: {get_url_data.original_url}")
        redis_key = f"short_url:{short_code}"
        update_cache(redis_key,get_url_data.original_url)
        update_db_visit_count(db.session, short_code)
        return redirect(get_url_data.original_url, 302)


## TRACING ##
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
import os

# Step 1: Create TracerProvider
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "url-shortener"})
    )
)

# Step 2: Create OTLP HTTP exporter (no 'insecure' argument)
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
logger.info(f"Using OTLP endpoint: {otlp_endpoint}")

otlp_exporter = OTLPSpanExporter(
    # endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
)

# Step 3: Add BatchSpanProcessor
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Step 4: Instrument Flask app
FlaskInstrumentor().instrument_app(app)


if __name__ == "__main__":
    app.run(debug=True, host= "0.0.0.0", port=5000)