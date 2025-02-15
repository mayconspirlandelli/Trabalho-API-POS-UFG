from dotenv import load_dotenv
import os
from groq import Groq
from fastapi import FastAPI, status, HTTPException, Request
import json
import chatbot


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



response_model=Resultado,
        summary="Multiplica dois numeros. Versão 3.0",
        description="Função responsável por receber dois números inteiros e retorna o produto.",
        tags=[GrupoNome.multiplicacao, GrupoNome.teste])



@app.post("/chatbot",
        summary="Endpoint para interação com o chatbot.",
        description=
        """
            ### Parâmetros:
            - **prompt** (str): Mensagem enviada pelo usuário ao chatbot.

            ### Retorno:
            - **mensagem** (dict): Resposta gerada pelo chatbot.
            """,
        tags=[GrupoNome.multiplicacao, GrupoNome.teste])
)
def chatbot(prompt: str):
    """
    Endpoint para interação com o chatbot.

    ### Parâmetros:
    - **prompt** (str): Mensagem enviada pelo usuário ao chatbot.

    ### Retorno:
    - **mensagem** (dict): Resposta gerada pelo chatbot.

    ### Exemplo de Requisição (JSON):
    ```json
    {
        "prompt": "Olá, como você está?"
    }
    ```

    ### Exemplo de Resposta:
    ```json
    {
        "mensagem": "Estou bem, obrigado! Como posso ajudar?"
    }
    ```
    """
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


