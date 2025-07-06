from sqlalchemy import select
from db.models import Links
import random, string

def check_short_key(session, key):
    return session.query(Links).filter(Links.short_url == key).first()

def add_to_db(session, original_url, short_url):
    new_url = Links(original_url=original_url, short_url=short_url)
    session.add(new_url)
    session.commit()

def generate_unique_short_code(session, length=6):
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        existing = check_short_key(session, short_code)
        if not existing:
            return short_code