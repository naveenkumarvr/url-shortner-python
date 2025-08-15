import pytest
from utils import utils

class DummySession:
    def __init__(self):
        self._data = {}
        self.added = None
        self.committed = False
    def query(self, model):
        self.model = model
        return self
    def filter(self, cond):
        self.cond = cond
        return self
    def first(self):
        # Simulate DB hit/miss based on test setup
        return self._data.get(getattr(self, "key", None), None)
    def add(self, obj):
        self.added = obj
        self._data[obj.short_url] = obj
    def commit(self):
        self.committed = True

class DummyLink:
    def __init__(self, original_url, short_url, visits=0):
        self.original_url = original_url
        self.short_url = short_url
        self.visits = visits

def test_check_short_key_found():
    session = DummySession()
    link = DummyLink("https://example.com", "abc123")
    session._data["abc123"] = link
    session.key = "abc123"
    result = utils.check_short_key(session, "abc123")
    assert result == link

def test_check_short_key_not_found():
    session = DummySession()
    session.key = "notfound"
    result = utils.check_short_key(session, "notfound")
    assert result is None

def test_add_to_db():
    session = DummySession()
    utils.add_to_db(session, "https://example.com", "abc123")
    assert session.added.original_url == "https://example.com"
    assert session.added.short_url == "abc123"
    assert session.committed is True


def test_generate_unique_short_code_returns_unique(monkeypatch):
    session = DummySession()
    # Always return None to simulate no collision
    monkeypatch.setattr(utils, "check_short_key", lambda s, k: None)
    code = utils.generate_unique_short_code(session, length=8)
    assert isinstance(code, str)
    assert len(code) == 8

def test_generate_unique_short_code_collision(monkeypatch):
    session = DummySession()
    # Simulate collision on first call, then success
    calls = [DummyLink("https://example.com", "abcdef"), None]
    def fake_check(s, k):
        return calls.pop(0)
    monkeypatch.setattr(utils, "check_short_key", fake_check)
    code = utils.generate_unique_short_code(session, length=6)
    assert isinstance(code, str)
    assert len(code) == 6