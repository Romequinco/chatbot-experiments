# WhatsApp Chatbot con Claude

Backend en FastAPI que recibe mensajes de WhatsApp Cloud API (Meta) y responde
usando Claude (Anthropic) como motor de inteligencia artificial.

## Requisitos

- Python 3.11+
- Una API key de Anthropic ([console.anthropic.com](https://console.anthropic.com))

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
# Abre .env y rellena ANTHROPIC_API_KEY y WHATSAPP_VERIFY_TOKEN
```

## Arranque

```bash
uvicorn app.main:app --reload --port 8000
```

## Probar sin credenciales de Meta

### 1. Verificación del webhook

```bash
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=mi_token_secreto&hub.challenge=12345"
# Respuesta esperada: 12345
```

> El valor de `hub.verify_token` debe coincidir con `WHATSAPP_VERIFY_TOKEN` en tu `.env`.

### 2. Simular un mensaje entrante

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "object": "whatsapp_business_account",
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "34600000000",
            "type": "text",
            "text": {"body": "Hola, ¿en qué consiste la comunidad?"}
          }]
        }
      }]
    }]
  }'
```

La respuesta de Claude aparece en la consola del servidor. El historial se
mantiene por número de teléfono (hasta 20 mensajes).

## Exponer con ngrok (para conectar Meta)

```bash
ngrok http 8000
# Copia la URL https://xxxx.ngrok.io y úsala como webhook URL en Meta Business
```

## Estructura

```
app/
  main.py           # App FastAPI + router
  webhook.py        # GET y POST /webhook
  claude_client.py  # Llamadas a Anthropic SDK
  conversation.py   # Historial en memoria por número
  whatsapp.py       # Parser de payloads Meta + envío futuro
```

## Variables de entorno

| Variable | Descripción |
|---|---|
| `ANTHROPIC_API_KEY` | API key de Anthropic |
| `WHATSAPP_VERIFY_TOKEN` | Token libre que defines tú para verificar el webhook |
| `WHATSAPP_TOKEN` | Token de acceso de Meta (cuando tengas credenciales) |
| `WHATSAPP_PHONE_ID` | ID del número de teléfono en Meta Business |
