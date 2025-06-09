from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Fake actuator input format
class ActuateRequest(BaseModel):
    decision: str  # Should be "ACCEPT" or "REJECT"

@app.get("/scan")
def get_scan():
    if random.random() < 0.2:
        raise HTTPException(status_code=500, detail="Scanner failure.")
    value = random.randint(0, 100)
    logging.info(f"[Scanner] Generated scan value: {value}")
    return {"scan_value": value}

@app.post("/actuate")
def actuate(request: ActuateRequest):
    if random.random() < 0.1:
        raise HTTPException(status_code=500, detail="Actuator failure.")
    logging.info(f"[Actuator] Triggered with decision: {request.decision}")
    return {"status": "success", "decision": request.decision}

@app.get("/")
def root():
    return {"message": "Welcome to the Scanner API. Use /scan, /classify, or /actuate."}
