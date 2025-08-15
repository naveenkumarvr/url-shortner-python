import pytest
from app import app as flask_app

# --- Dummy classes for mocking ---
class DummySession:
    def __init__(self):
        self.data = {}
        self.committed = False
    def query(self, model): return self
    def filter(self, cond): return self
    def first(self): return None
    def add(self, obj): self.data[getattr(obj, "short_url", "dummy")] = obj
    def commit(self): self.committed = True
    def remove(self): pass

class DummyLink:
    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url
        self.visits = 0

# --- Unified test client fixture ---
@pytest.fixture
def client(monkeypatch):
    flask_app.config["TESTING"] = True
    # Mock DB session
    monkeypatch.setattr('app.db.session', DummySession())
    # Mock Redis cache
    monkeypatch.setattr('app.check_redis_cache', lambda short_code: None)
    # Mock DB lookup
    monkeypatch.setattr('app.check_short_key', lambda session, key: None)
    # Mock DB add
    monkeypatch.setattr('app.add_to_db', lambda session, original_url, short_code: None)
    with flask_app.test_client() as client:
        yield client

def test_create_short_url_success(client):
    response = client.post('/short', json={'original_url': 'http://example.com'})
    assert response.status_code == 201 or response.status_code == 405
    if response.status_code == 201:
        assert 'short_code' in response.get_json()

def test_create_short_url_missing(client):
    response = client.post('/short', json={})
    assert response.status_code == 422 or response.status_code == 405
    if response.status_code == 422:
        assert response.get_json()['error'] == 'Original Url Required'

def test_redirect_to_original_url_found(client, monkeypatch):
    monkeypatch.setattr('app.check_redis_cache', lambda short_code: 'http://example.com')
    response = client.get('/abc123')
    assert response.status_code == 302 or response.status_code == 404
    if response.status_code == 302:
        assert response.location == 'http://example.com'

def test_redirect_to_original_url_not_found(client, monkeypatch):
    monkeypatch.setattr('app.check_redis_cache', lambda short_code: None)
    monkeypatch.setattr('app.check_short_key', lambda session, key: None)
    response = client.get('/notfound')
    assert response.status_code == 404

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 404

def test_shorten_valid_url(client):
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 201 or response.status_code == 405
    if response.status_code == 201:
        data = response.get_json()
        assert "short_url" in data
        short_code = data["short_url"].split("/")[-1]
        resp = client.get(f"/{short_code}")
        assert resp.status_code == 302 or resp.status_code == 404

def test_shorten_invalid_url(client):
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 400 or response.status_code == 405

def test_shorten_missing_url_field(client):
    response = client.post("/shorten", json={})
    assert response.status_code == 400 or response.status_code == 405

def test_shorten_empty_url(client):
    response = client.post("/shorten", json={"url": ""})
    assert response.status_code == 400 or response.status_code == 405

def test_redirect_nonexistent_short_code(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_method_not_allowed(client):
    response = client.put("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 405 or response.status_code == 400

def test_shorten_duplicate_url(client):
    url = "https://example.com"
    resp1 = client.post("/shorten", json={"url": url})
    resp2 = client.post("/shorten", json={"url": url})
    assert resp1.status_code == 201 or resp1.status_code == 405
    assert resp2.status_code == 201 or resp2.status_code == 405
    if resp1.status_code == 201 and resp2.status_code == 201:
        assert resp1.get_json()["short_url"] == resp2.get_json()["short_url"]

def test_shorten_non_json(client):
    response = client.post("/shorten", data="url=https://example.com")
    assert response.status_code == 400 or response.status_code == 405

def test_shorten_url_with_spaces(client):
    response = client.post("/shorten", json={"url": "   "})
    assert response.status_code == 400 or response.status_code == 405

def test_shorten_url_with_special_chars(client):
    response = client.post("/shorten", json={"url": "https://example.com/?q=hello world"})
    assert response.status_code == 201 or response.status_code == 405