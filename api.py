from dotenv import load_dotenv
import os
from groq import Groq
from fastapi import FastAPI, status, HTTPException, Request
import json
from executar_groq import executar_groq

app = FastAPI(
    title="Assistente de Pedidos",
    description="Agente inteligente responsável por auxiliar o chef de cozinha durante a gestão de pedidos de um delivery",
    summary="",
    version="1.0",
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



@app.post("/chatbot",
        summary="Endpoint para interação com o chatbot.",
        description=
        """
            ### Parâmetros:
            - prompt (str): Mensagem enviada pelo usuário ao chatbot.

            Retorno:
            - mensagem: Resposta gerada pelo chatbot.
            """,
        )
def chatbot(prompt: str):
    resultado = executar_groq(prompt)
    print(resultado)
    return {"mensagem": resultado}


# Webhook para receber pedidos
@app.post("/webhook/",
    summary="Receber Webhook do Ifood",
    description="""
    Este endpoint recebe um webhook do Ifood e invoca o assistente inteligente.

    ### Funcionamento:
    1. Captura os dados enviados no webhook em formato JSON.
    2. Converte os dados em uma string JSON formatada.
    3. Registra os dados recebidos no log.
    4. Envia os dados para o chatbot processá-los.
    5. Retorna uma mensagem de sucesso.

    ### Exemplo de Requisição:
    ```json
    {
        "id_pedido": 12345,
        "cliente": "João Silva",
        "produtos": [
            {"nome": "Teclado Mecânico", "quantidade": 1},
            {"nome": "Mouse Gamer", "quantidade": 1}
        ],
        "total": 350.00
    }
    ```

    ### Exemplo de Resposta:
    ```json
    {
        "message": "Webhook processado com sucesso!"
    }
    ```

    ### Códigos de Resposta:
    - `200`: Webhook recebido e processado com sucesso.
    - `400`: Erro ao processar o webhook (caso necessário adicionar validações futuras).
    """)
async def receber_webhook(request: Request):
    pedido_json = await request.json()  # Captura os dados enviados no webhook
    
    pedido = json.dumps(pedido_json, indent=4, ensure_ascii=False)
    print(f"Webhook recebido: \n {pedido}")  # Log dos dados recebidos

    chatbot(pedido)  # Chama o chatbot com os dados do pedido
    return {"message": "Webhook processado com sucesso!"}


