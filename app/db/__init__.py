from flask_sqlalchemy import SQLAlchemy

# Creating the SQLAlchemy instance
db = SQLAlchemy()

# ReImporting models so that can be called by other module directly
from .models import Links