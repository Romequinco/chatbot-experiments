import os
import httpx
from dotenv import load_dotenv

load_dotenv()


def parse_incoming(payload: dict) -> tuple[str, str] | None:
    """Extract (phone, text) from a WhatsApp Cloud API webhook payload.

    Returns None if the payload contains no text message.
    """
    try:
        messages = (
            payload["entry"][0]["changes"][0]["value"].get("messages", [])
        )
        if not messages:
            return None
        msg = messages[0]
        if msg.get("type") != "text":
            return None
        phone = msg["from"]
        text = msg["text"]["body"]
        return phone, text
    except (KeyError, IndexError):
        return None

async def send_message(phone: str, text: str) -> None:
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != 200:
            print(f"[ERROR Meta API] {response.status_code}: {response.text}")
        else:
            print(f"[OK] Mensaje enviado a {phone}")
