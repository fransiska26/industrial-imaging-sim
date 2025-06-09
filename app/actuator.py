import random
import requests

# Simulated Actuator
class Actuator:
    def __init__(self):
        self.endpoint = None

    def trigger(self, decision):
        # Simulate actuator failure with 10% chance
        if random.random() < 0.1:
            raise RuntimeError("Actuator failure.")
        
    def trigger_request(self, decision):
        if self.endpoint == None:
            raise ValueError("Endpoint is not defined")
            return
        payload = {"decision": decision}
        response = requests.post(self.endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        return result

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint