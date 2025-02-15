import requests
import json
from fastapi import FastAPI, status, HTTPException, Depends

def carrega_pedido_json():
    # Abrindo e carregando o JSON
    with open("pedido.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)  
        if dados == null:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Não foi possível carregar arquivo JSON") 
        
        pedido_json = json.dumps(dados, indent=4, ensure_ascii=False) # Converte JSON para dicionário Python

    #print(pedido_json)
    return pedido_json


def registrar_webhook():
    # Convertendo para JSON
    dados_carregado = carrega_pedido_json()
    if dados_carregado == null:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Não foi possível carregar arquivo JSON") 
    print(json_pedido)
   
    
    #Envia Webhook, simulando o recebimento de um pedido via ifood
    link = "https://humble-space-rotary-phone-x75x5jjprwhpjwj-8000.app.github.dev/webhook/"
    
    response = requests.post(link, data=json_pedido)
    #print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")

if __name__ == "__main__":
    #registrar_webhook()  # Executa a função ao rodar o script
    carrega_pedido_json()
