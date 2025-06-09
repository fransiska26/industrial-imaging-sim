import random
import requests

# Simulated Scanner
class Scanner:
    def __init__(self):
        self.latest_scan = None
        self.endpoint = None

    def read(self):
        # Simulate sensor failure with 20% chance
        if random.random() < 0.2:
            raise RuntimeError("Scanner malfunction detected.")
        self.latest_scan = random.randint(0, 100)
        return self.latest_scan
    
    def read_request(self):
        if self.endpoint == None:
            raise ValueError("Endpoint is not defined")
            return
        response = requests.get(self.endpoint)
        response.raise_for_status()
        data = response.json()
        return data["scan_value"]


    def set_endpoint(self, endpoint):
        self.endpoint = endpoint
