import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = (
    "Eres un asistente amable y respetuoso que ayuda a personas interesadas "
    "en unirse a una comunidad privada de pago. Tu objetivo es resolver dudas, "
    "generar confianza y guiar al usuario hacia la decisión de unirse. "
    "Mantén siempre un tono cálido, cercano y profesional."
)

_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def send_message(history: list[dict]) -> str:
    """Send the full conversation history to Claude and return the reply text."""
    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    return response.content[0].text
