import random

# Simulated Processor (AI model)
class Processor:
    def __init__(self):
        pass

    def classify(self, scan_value):
        # Dummy classification: above threshold = "Reject"
        return "REJECT" if scan_value > 50 else "ACCEPT"