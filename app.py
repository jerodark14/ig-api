from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "meu_token_secreto"

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge)
    return {"error": "Verificação falhou"}
