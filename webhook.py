import requests
import json
from fastapi import FastAPI, status, HTTPException, Depends
import logging

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')


def carrega_pedido_json():
    try:
        # Abrindo e carregando o JSON
        with open("pedido.json", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()  # Remove espaços em branco

            if not conteudo or conteudo in ["null", "{}", "[]"]:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O arquivo contém um JSON nulo ou vazio.") 
            else:
                dados = json.loads(conteudo)  # Tenta carregar o JSON
                #print("O JSON contém:", dados)
                pedido_json = json.dumps(dados, indent=4, ensure_ascii=False) # Converte JSON para dicionário Python

        return pedido_json

    except Exception as e:
        logging.error(f"Erro: {e}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Não foi possível carregar arquivo JSON") 


def registrar_webhook():
    dados_carregado = carrega_pedido_json()
    
    #Envia Webhook, simulando o recebimento de um pedido via ifood
    link = "https://humble-space-rotary-phone-x75x5jjprwhpjwj-8000.app.github.dev/webhook/"
    
    response = requests.post(link, data=dados_carregado)
    #print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")

if __name__ == "__main__":
    carrega_pedido_json() # Executa a função ao rodar o script
