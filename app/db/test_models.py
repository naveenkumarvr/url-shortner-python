import pytest

# Import your model (adjust if needed)
from db.models import Links

def test_links_model_creation():
    link = Links(original_url="https://example.com", short_url="abc123", visits=0)
    assert link.original_url == "https://example.com"
    assert link.short_url == "abc123"
    assert link.visits == 0

def test_links_repr():
    link = Links(original_url="https://example.com", short_url="abc123", visits=0)
    rep = repr(link)
    assert "abc123" in rep
    assert "example.com" in rep

def test_links_update_visits():
    link = Links(original_url="https://example.com", short_url="abc123", visits=0)
    link.visits += 1
    assert link.visits == 1

def test_links_equality():
    link1 = Links(original_url="https://example.com", short_url="abc123", visits=0)
    link2 = Links(original_url="https://example.com", short_url="abc123", visits=0)
    assert link1.short_url == link2.short_url
    assert link1.original_url == link2.original_url


def test_links_empty_fields():
    link = Links(original_url="", short_url="", visits=0)
    assert link.original_url == ""
    assert link.short_url == ""
    assert link.visits == 0

def test_links_none_fields():
    link = Links(original_url=None, short_url=None, visits=None)
    assert link.original_url is None
    assert link.short_url is None
    assert link.visits is None

def test_links_negative_visits():
    link = Links(original_url="https://example.com", short_url="abc123", visits=-5)
    assert link.visits == -5