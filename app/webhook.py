import os
from fastapi import APIRouter, Request, Response, HTTPException
from dotenv import load_dotenv

from app.conversation import store
from app.claude_client import send_message
from app.whatsapp import parse_incoming

load_dotenv()

router = APIRouter()


@router.get("/webhook")
def verify_webhook(request: Request):
    """Meta calls this endpoint to verify the webhook URL during setup."""
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == os.getenv("WHATSAPP_VERIFY_TOKEN"):
        return Response(content=challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/webhook")
async def receive_message(request: Request):
    """Receive incoming WhatsApp messages from Meta."""
    payload = await request.json()

    # Ignore non-WhatsApp payloads silently (Meta sends other event types)
    if payload.get("object") != "whatsapp_business_account":
        return {"status": "ignored"}

    result = parse_incoming(payload)
    if result is None:
        return {"status": "no_text_message"}

    phone, text = result

    store.append(phone, "user", text)
    reply = send_message(store.get(phone))
    store.append(phone, "assistant", reply)

    print(f"\n[{phone}] User: {text}")
    print(f"[{phone}] Claude: {reply}\n")

    # TODO: uncomment when Meta credentials are available
    # await whatsapp.send_message(phone, reply)

    return {"status": "ok"}
