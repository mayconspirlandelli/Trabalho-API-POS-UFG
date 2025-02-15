from dotenv import load_dotenv
import os
from groq import Groq
from fastapi import FastAPI, status, HTTPException, Request
import json


app = FastAPI(
    title="Assistente de Pedidos",
    description="",
    summary="",
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
                "name": "Maycon",
                "url": "http://github.com/mayconspirlandelli",
                "email": "maycon@ufg.br",
    },
            license_info={
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }, )


def executar_groq(mensagem_usuario):
    try:
        # Carrega a chave da API
        load_dotenv()
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
      
        if not GROQ_API_KEY:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Chave da API do Groq não encontrada no .env") 

        # Conecta ao Groq
        client = Groq(api_key=GROQ_API_KEY,)

        # Configura o comportamento do chatbot
        system_prompt = {
            "role": "system",            
            "content": """Você assume o papel de assistente virtual responsável por gerenciar 
                os pedidos que chega na confeitaria de doces que você trabalha. Seu papel é auxiliar
                a chef de cozinha. Sua função é descrever os pedidos que chegarem via plataforma do ifood. 
                Você deve ler a descrição do pedido para chef de cozinha informando os seguintes dados do pedido: 
                Número do pedido, nome do cliente, informar quantos pedidos o cliente já fez ou se já é um
                cliente novato, nome do produtos e sua respectiva quantidade, calcule o valor total do pedido."""
        }

        # Inicializa o histórico de mensagens
        chat_history = [system_prompt]
        chat_history.append({"role": "user", "content": mensagem_usuario})

        # Faz a chamada à API
        response = client.chat.completions.create(
            messages=chat_history,
            model="llama3-8b-8192",
            temperature=0.7,
            max_completion_tokens=200,
        )

        # Extrai a resposta do assistente
        resposta_assistente = response.choices[0].message.content.strip()
        return resposta_assistente

    except Exception as e:
        # Log do erro (pode ser substituído por um logger)
        print(f"Erro ao se comunicar com o Groq: {e}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Ocorreu um erro ao processar sua solicitação.") 
    

@app.post("/chatbot")
def chatbot(prompt: str):
    resultado = executar_groq(prompt)
    print(resultado)
    return {"mensagem": resultado}


# Webhook para receber pedidos
@app.post("/webhook/")
async def receber_webhook(request: Request):
    pedido_json = await request.json()  # Captura os dados enviados no webhook
    
    pedido = json.dumps(pedido_json, indent=4, ensure_ascii=False)
    print(f"Webhook recebido: \n {pedido}")  # Log dos dados recebidos

    chatbot(pedido)  # Chama o chatbot com os dados do pedido
    return {"message": "Webhook processado com sucesso!"}


