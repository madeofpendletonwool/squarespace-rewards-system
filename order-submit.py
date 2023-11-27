from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import hashlib
import hmac
import uvicorn

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    # Your Squarespace webhook secret
    webhook_secret = 'your_webhook_secret'

    # Retrieve the body and signature from the request
    body = await request.body()
    signature = request.headers.get('Squarespace-Signature')

    # Verify the Squarespace signature
    if not is_valid_signature(body, signature, webhook_secret):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # Process the webhook payload
    payload = await request.json()
    process_order(payload['data'])

    return JSONResponse(content={'status': 'success'})


def is_valid_signature(payload, signature, secret):
    hmac_new = hmac.new(secret.encode(), payload, hashlib.sha256)
    return hmac.compare_digest(hmac_new.hexdigest(), signature)


def process_order(order_data):
    print(order_data)
    # Logic to process order data and update Google Sheets
    # ...


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
