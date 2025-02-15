import requests
import json
from fastapi import FastAPI, Request

app = FastAPI()


# Substitua pelo token do seu bot
API_TOKEN = ""
TELEGRAM_API_URL = f"https://api.telegram.org/bot{API_TOKEN}"

# Configuração básica do logger
#logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

APP_LINK="https://didactic-yodel-76vwvgg9q9cv4x-8000.app.github.dev"




# Endpoint para o webhook do Telegram
@app.post("/telegram/")
async def webhook(request: Request):
    """
    Recebe atualizações do Telegram e processa mensagens recebidas.
    """
    payload = await request.json()  # Captura os dados enviados pelo Telegram

    # Verifica se a mensagem contém um texto
    if "message" in payload:
        message = payload["message"]
        chat_id = message["chat"]["id"]
        text = message["text"]

        # Responde a mensagem recebida com uma confirmação
        enviar_mensagem_telegram(chat_id, f"Você disse: {text}")

    return {"status": "success"}

def enviar_mensagem_telegram(chat_id: int, text: str):
    """
    Envia uma mensagem para um chat no Telegram.
    
    Parâmetros:
    - chat_id (int): ID do chat do Telegram para enviar a mensagem.
    - text (str): Texto da mensagem a ser enviada.
    """
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    # Envia a mensagem via POST
    response = requests.post(url, data=payload)
    print(f"Mensagem enviada: {response.status_code} - {response.text}")

# Configuração do Webhook do Telegram (a primeira vez que você configurar)
@app.on_event("startup")
async def configurar_webhook():
    """
    Configura o Webhook do Telegram para que ele envie as mensagens para o nosso servidor.
    """
    #webhook_url = "https://your-domain.com/webhook/"  # Substitua pela URL do seu servidor
    webhook_url = APP_LINK + "/telegram/" 
    url = f"{TELEGRAM_API_URL}/setWebhook?url={webhook_url}"

    response = requests.get(url)
    print(f"Webhook configurado: {response.status_code} - {response.text}")


if __name__ == "__main__":
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": "Sua mensagem aqui"}
    response = requests.post(url, data=payload)
