
import pytest
from flask import Flask
from app import app as flask_app
import json

class DummySession:
    def __init__(self):
        self.data = {}
        self.committed = False
    def query(self, model):
        return self
    def filter(self, cond):
        return self
    def first(self):
        return None
    def add(self, obj):
        self.data[obj.short_url] = obj
    def commit(self):
        self.committed = True
    def remove(self):
        pass

class DummyLink:
    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url
        self.visits = 0

def test_create_short_url_success(monkeypatch):
    """
    Test that a valid POST to /short returns a short URL.
    Mocks DB session and utility functions to isolate logic.
    Expects status 201 and a short_code in response.
    """
    client = flask_app.test_client()
    monkeypatch.setattr('app.db.session', DummySession())
    monkeypatch.setattr('app.check_short_key', lambda session, key: None)
    monkeypatch.setattr('app.add_to_db', lambda session, original_url, short_code: None)
    response = client.post('/short', json={'original_url': 'http://example.com'})
    assert response.status_code == 201
    assert 'short_code' in response.get_json()

def test_create_short_url_missing(monkeypatch):
    """
    Test that a POST to /short without original_url returns error 422.
    Checks for correct error message in response.
    """
    client = flask_app.test_client()
    response = client.post('/short', json={})
    assert response.status_code == 422
    assert response.get_json()['error'] == 'Original Url Required'

def test_redirect_to_original_url_found(monkeypatch):
    """
    Test that a GET to /<short_code> returns a redirect (302) if found in cache.
    Mocks Redis cache to return a URL.
    """
    client = flask_app.test_client()
    monkeypatch.setattr('app.check_redis_cache', lambda short_code: 'http://example.com')
    response = client.get('/abc123')
    assert response.status_code == 302
    assert response.location == 'http://example.com'

def test_redirect_to_original_url_not_found(monkeypatch):
    """
    Test that a GET to /<short_code> returns 404 if not found in cache or DB.
    Mocks both Redis and DB lookup to return None.
    """
    client = flask_app.test_client()
    monkeypatch.setattr('app.check_redis_cache', lambda short_code: None)
    monkeypatch.setattr('app.check_short_key', lambda session, key: None)
    response = client.get('/notfound')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Not Found'