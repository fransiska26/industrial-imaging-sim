import time
import logging
import os
from app.scanner import Scanner
from app.processor import Processor
from app.actuator import Actuator

endpoint = os.getenv("ENDPOINT", "http://api:8000")  # fallback value
num_retry = int(os.getenv("NUM_RETRY", "5"))
num_cycle = int(os.getenv("NUM_CYCLE", "2"))

# Initialize Logger
logger = logging.getLogger("scanner_system")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Controller:
    def __init__(self, logger):
        self.logger = logger
        self.scanner = Scanner()
        self.processor = Processor()
        self.actuator = Actuator()

    def set_logger(self, logger):
        self.logger = logger

    # Controller logic
    def run_once(self):
        try:
            scan = self.scanner.read()
            self.logger.info(f"[Scanner] Scan value: {scan}")
            decision = self.processor.classify(scan)
            self.logger.info(f"[Processor] Classification: {decision}")
            self.actuator.trigger(decision)
            return True
        except RuntimeError as e:
            self.logger.error(str(e))
            return False


    def run_cycles(self, cycles_num, numoftry):
        for i in range(cycles_num):
            success = False
            cycle_logger = CycleLogger(logger, {'iteration': i})
            self.set_logger(cycle_logger)

            for i in range(numoftry+1): 
                success = self.run_once()
                if success:
                    break
                else:
                    time.sleep(0.5)
            
            if not success:
                self.logger.warning("All retry attempts failed")

class ControllerWithHTTPAPI(Controller):
    def __init__(self, logger, endpoint):
        super().__init__(logger)
        self.scanner.set_endpoint(f"{endpoint}/scan")
        self.actuator.set_endpoint(f"{endpoint}/actuate")

    def run_once(self):
        try:
            scan = self.scanner.read_request()
            self.logger.info(f"[Scanner] Scan value: {scan}")
        except Exception as e:
            self.logger.error(f"[Scanner] {str(e)}")
            return False
        decision = self.processor.classify(scan)
        self.logger.info(f"[Processor] Classification: {decision}")
        
        try:
            result= self.actuator.trigger_request(decision)
            self.logger.info(f"[Actuator] Actuator result: {result}")
            return True
        except Exception as e:
            self.logger.error(f"[Actuator] {str(e)}")
            return False

        


class CycleLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[Cycle {self.extra['iteration']}] {msg}", kwargs

# Run one simulation step
if __name__ == "__main__":
    endpoint = "http://api:8000"
    controller = Controller(logger)
    # controller = Controller(logger=None)
    controller = ControllerWithHTTPAPI(logger, endpoint)    
    controller.run_cycles(num_cycle, num_retry)