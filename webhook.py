import requests
import json
import logging
from dotenv import load_dotenv
import os

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

#APP_LINK="https://didactic-yodel-76vwvgg9q9cv4x-8000.app.github.dev"


def carregar_link():
    load_dotenv()
    APP_LINK = os.environ.get("APP_LINK")
    if not APP_LINK :
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Link inválido") 
    
    logging.info("Link correto!")
    return APP_LINK


def carrega_pedido_json():
    try:
        # Abrindo e carregando o JSON
        with open("pedido.json", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()  # Remove espaços em branco

            if not conteudo or conteudo in ["null", "{}", "[]"]:
                #raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="O arquivo contém um JSON nulo ou vazio.") 
                logging.error(f"Erro: O arquivo contém um JSON nulo ou vazio.")
            else:
                dados = json.loads(conteudo)  # Tenta carregar o JSON
                #print("O JSON contém:", dados)
                pedido_json = json.dumps(dados, indent=4, ensure_ascii=False) # Converte JSON para dicionário Python

        return pedido_json

    except Exception as e:
        logging.error(f"Erro: {e} - Não foi possível carregar arquivo JSON")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Não foi possível carregar arquivo JSON") 


def registrar_webhook():
    dados_carregado = carrega_pedido_json()

    # Definição do token de autenticação
    api_token = "123"

    # Cabeçalhos da requisição (Authorization Bearer)
    headers = {
        "Authorization": f"{api_token}",
        "Content-Type": "application/json"
    }
    
    #Envia Webhook, simulando o recebimento de um pedido via ifood
    link = carregar_link() + "/webhook/"
    
    response = requests.post(link, data=dados_carregado, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")

if __name__ == "__main__":
    registrar_webhook() # Executa a função ao rodar o script
