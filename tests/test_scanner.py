import pytest
from app.scanner import Scanner
import random

def test_scanner_read_success(monkeypatch):
    # Always return a safe random value
    monkeypatch.setattr(random, "random", lambda: 0.5)  # No failure
    scanner = Scanner()
    value = scanner.read()
    assert isinstance(value, int)
    assert 0 <= value <= 100

def test_scanner_read_failure(monkeypatch):
    # Force failure condition
    monkeypatch.setattr(random, "random", lambda: 0.1)  # Below 0.2 → trigger failure
    scanner = Scanner()
    with pytest.raises(RuntimeError, match="Scanner malfunction detected."):
        scanner.read()
