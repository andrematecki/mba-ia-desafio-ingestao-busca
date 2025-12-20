# Desafio MBA Engenharia de Software com IA - Full Cycle


## Setup ambiente
1. Instalar virtual enviroment para execução do script Python. Na raiz do projeto, execute:
```shell
#criando virtualenv
python -m venv venv
#ativando virtualenv
source venv/bin/activate
```

2. Instalar dependencias
```shell
pip install -r requirements.txt
```

3. Crie o arquivo ".env" na raiz do projeto a partir do ".env.example". Preencha as variaveis:
    
- OPENAI_API_KEY : API Key da Open AI

## Execução do codigo

1. Subir o banco de dados:

``` shell
docker compose up -d
```

2. Executar ingestão do PDF (somente primeira vez):

```shell
python src/ingest.py
```

3. Rodar o chat:
```shell
python src/chat.py
```
