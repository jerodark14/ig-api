from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "meu_token_secreto"


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)

    return {"error": "Verificação falhou"}
