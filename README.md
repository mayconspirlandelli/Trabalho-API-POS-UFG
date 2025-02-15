# Trabalho-API-POS-UFG
Trabalho da Disciplina API FastAPI do prof Rogerio da Pós Agentes Inteligentes do INF-UFG


- Para iniciar a configuraçoes inicais
```
python -m venv .venv
source .venv/bin/activate
pip install -r requuirements.txt
pip install -—upgrade pip
```

- Alterar o link no arquivo .env na tag APP_LINK

- Alterar o nome do *env-exemplo* para *.env* 

- Configurar a chave, token, link da aplicação.

- Se tiver usando a maquina Codespace do Github, configurar a PORTA com *public*

- Para instalar a biblioteca FastAPI
``` pip install "fastapi[standard]" ```

- Para instalar a biblioteca para usar o Dotenv pra carregar configuracoes e chaves api 
``` pip install python-dotent ```

- Para instalar o GROQ, orquestrador de LLM
``` pip install groq ```

- Crie o arquivo *main.py*

- Pra rodar o projeto Fastapi
``` fastapi dev main.py ```

- Pra rodar o webhook
``` python webhook.py ```
