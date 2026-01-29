from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

# ✅ TOKEN DE VERIFICAÇÃO DO WEBHOOK (simples)
VERIFY_TOKEN = "meu_token_webhook_123"


@app.get("/")
def home():
    return {"status": "ok"}


# ✅ VERIFICAÇÃO DO WEBHOOK (GET)
@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)

    return PlainTextResponse("Verificação falhou", status_code=403)


# ✅ RECEBER EVENTOS (POST) - aqui chegam mensagens e status
@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    # 1) mostra o JSON bruto
    print("📩 Webhook recebido:", data)

    # 2) tenta extrair texto e status
    try:
        entry = data.get("entry", [])[0]
        change = entry.get("changes", [])[0]
        value = change.get("value", {})

        # mensagem real
        if "messages" in value:
            msg = value["messages"][0]
            from_number = msg.get("from")

            text = None
            if msg.get("type") == "text":
                text = msg.get("text", {}).get("body")

            print(f"✅ MENSAGEM: de={from_number} texto={text}")

        # status (entregue, lida, etc.)
        if "statuses" in value:
            st = value["statuses"][0]
            print(
                f"✅ STATUS: id={st.get('id')} status={st.get('status')} "
                f"timestamp={st.get('timestamp')} recipient={st.get('recipient_id')}"
            )

    except Exception as e:
        print("⚠️ Erro ao processar webhook:", e)

    return {"status": "received"}
