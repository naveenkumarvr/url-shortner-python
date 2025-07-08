from sqlalchemy import select
from db.models import Links
import random, string

def check_short_key(session, key):
    """
    Check whether the short key present in the DB if present returns the row
    INPUTS:
        session(Obj): Db session object
        key(str): short code
    RETURNS:
        query_results(dict): Query result of specific row
    """
    return session.query(Links).filter(Links.short_url == key).first()

def add_to_db(session, original_url, short_url):
    """
    Add new url details to db
    INPUTS:
        session(Obj): Db session object
        short_url(str): short code
        original_url(str): Original Url

    """
    new_url = Links(original_url=original_url, short_url=short_url)
    session.add(new_url)
    session.commit()

def update_db_visit_count(session,short_code):
    """
    Updates the db visit code of corresponding Short code
    INPUTS:
        session(Obj): Db session object
        short_code(str): Short code
    RETURNS: none
    """
    url_details = check_short_key(session, short_code)
    url_details.visits += 1
    session.commit()


def generate_unique_short_code(session, length=6):
    """
    This generates unique short code of lenght 6 character and cross check that it is not present in db. Uses random_choices to do that.
    INPUTS:
        session(Obj): Db session object
        length(int): No of char. Default to 6
    RETURNS:
        short_code(str): Returns short code

    """
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        existing = check_short_key(session, short_code)
        if not existing:
            return short_code