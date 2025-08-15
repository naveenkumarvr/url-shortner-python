import pytest
from utils import redis as redis_module

class DummyRedisClient:
    def __init__(self):
        self.data = {}
    def get(self, key):
        return self.data.get(key)
    def setex(self, key, expiry, value):
        self.data[key] = value
        return True

def test_check_redis_cache_hit(monkeypatch):
    dummy_client = DummyRedisClient()
    dummy_client.data["short_url:abc123"] = "https://example.com"
    monkeypatch.setattr(redis_module, "redis_client", dummy_client)
    result = redis_module.check_redis_cache("abc123")
    assert result == "https://example.com"

def test_check_redis_cache_miss(monkeypatch):
    dummy_client = DummyRedisClient()
    monkeypatch.setattr(redis_module, "redis_client", dummy_client)
    result = redis_module.check_redis_cache("notfound")
    assert result is None

def test_update_cache(monkeypatch):
    dummy_client = DummyRedisClient()
    monkeypatch.setattr(redis_module, "redis_client", dummy_client)
    redis_module.update_cache("xyz789", "https://another.com")
    assert dummy_client.data["xyz789"] == "https://another.com"

def test_update_cache_overwrite(monkeypatch):
    dummy_client = DummyRedisClient()
    dummy_client.data["xyz789"] = "https://old.com"
    monkeypatch.setattr(redis_module, "redis_client", dummy_client)
    redis_module.update_cache("xyz789", "https://new.com")
    assert dummy_client.data["xyz789"] == "https://new.com"

def test_update_cache_with_empty_url(monkeypatch):
    dummy_client = DummyRedisClient()
    monkeypatch.setattr(redis_module, "redis_client", dummy_client)
    redis_module.update_cache("empty", "")
    assert dummy_client.data["empty"] == ""