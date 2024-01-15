from fastapi import FastAPI, HTTPException, Depends, Query
import requests
from config.config import Config

app = FastAPI()

VERIFY_TOKEN = "your_whatsapp_verify_token"

@app.get("/webhook")
async def verify_webhook(
    mode: str = Query(...),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(...),
):
    try:
        # Check if the mode and token sent are correct
        if mode == "subscribe" and token == VERIFY_TOKEN:
            # Respond with 200 OK and challenge token from the request
            print("WEBHOOK_VERIFIED")
            return {"challenge": challenge}

        # Responds with '403 Forbidden' if verify tokens do not match
        raise HTTPException(status_code=403, detail="Invalid verify token")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))