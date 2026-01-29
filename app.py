from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

# 🔐 TOKEN SIMPLES DE VERIFICAÇÃO DO WEBHOOK
VERIFY_TOKEN = "meu_token_webhook_123"


@app.get("/")
def home():
    return {"status": "ok"}


# ✅ VERIFICAÇÃO DO WEBHOOK (META / WHATSAPP)
@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse("Verificação falhou", status_code=403)


# 📩 RECEBER EVENTOS DO WHATSAPP (POST)
@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("📩 Webhook recebido:", data)
    return {"status": "received"}
