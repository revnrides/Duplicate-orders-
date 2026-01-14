from fastapi import FastAPI, Request
import hashlib

app = FastAPI()

# Store recent orders in memory
recent_orders = set()

@app.get("/")
def home():
    return {"status": "Duplicate Order Guard running"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    # Get order number or unique id
    order_id = str(data.get("id", ""))

    # Create fingerprint
    fingerprint = hashlib.md5(order_id.encode()).hexdigest()

    if fingerprint in recent_orders:
        return {"duplicate": True, "action": "blocked"}

    recent_orders.add(fingerprint)

    return {"duplicate": False, "action": "allowed"}
