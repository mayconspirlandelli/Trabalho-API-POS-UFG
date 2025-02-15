from dotenv import load_dotenv
import os
from groq import Groq
from fastapi import FastAPI, status, HTTPException, Request
import json
import logging

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(message)s')

def executar_groq(mensagem_usuario) -> str:
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
        logging.error(f"Erro ao se comunicar com Groq: {e}")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Ocorreu um erro ao processar sua solicitação.") 
