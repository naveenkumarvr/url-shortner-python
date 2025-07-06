import datetime
from db import db  # Import the db instance from __init__.py

# Defining the Links table
class Links(db.Model):
    __tablename__ = 'url_shortner'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_url = db.Column(db.String(18), unique=True, nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Link {self.short_url} -> {self.original_url}>'
