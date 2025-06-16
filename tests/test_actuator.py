import pytest
from app.actuator import Actuator
import random
import requests

def test_actuator_trigger_success(monkeypatch):
    # Force success by returning high value (e.g. 0.9) → no failure
    monkeypatch.setattr(random, "random", lambda: 0.9)
    
    actuator = Actuator()
    
    # Should not raise any exceptions
    try:
        actuator.trigger("ACCEPT")
    except RuntimeError:
        pytest.fail("Unexpected RuntimeError raised on success path.")


def test_actuator_trigger_failure(monkeypatch):
    # Force failure condition
    monkeypatch.setattr(random, "random", lambda: 0.05)  # Below 0.2 → trigger failure
    actuator = Actuator()
    with pytest.raises(RuntimeError, match="Actuator failure."):
        actuator.trigger("ACCEPT")


def test_trigger_request_success(monkeypatch):
    # Create mock response
    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return {"status": "success", "decision": "ACCEPT"}

    def mock_post(url, json):
        return MockResponse()

    # Apply monkeypatch
    monkeypatch.setattr(requests, "post", mock_post)

    # Run test
    actuator = Actuator()
    actuator.set_endpoint("http://dummy-endpoint/actuate")
    result = actuator.trigger_request("ACCEPT")
    assert result == {"status": "success", "decision": "ACCEPT"}