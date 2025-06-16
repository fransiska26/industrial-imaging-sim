import requests

BASE_URL = "http://localhost:8000"

def test_scan_success():
    response = requests.get(f"{BASE_URL}/scan")
    assert response.status_code == 200
    assert "scan_value" in response.json()


def test_actuate_invalid_input():
    # Send invalid data (missing or malformed decision)
    invalid_payloads = [
        {},  # Missing field
        {"decision": 123},  # Wrong type
        {"value": "REJECT"},  # Wrong key
    ]

    for payload in invalid_payloads:
        response = requests.post(f"{BASE_URL}/actuate", json=payload)
        assert response.status_code == 422
