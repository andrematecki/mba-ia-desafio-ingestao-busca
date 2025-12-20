import os
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector  
load_dotenv()


def validate_env_vars():
    """
    Valida a presença de variáveis de ambiente obrigatórias.
    
    Verifica se todas as variáveis de ambiente necessárias para a execução
    da aplicação estão definidas no sistema.
    
    Variáveis obrigatórias:
        - OPENAI_API_KEY: Chave de API do OpenAI
        - DATABASE_URL: URL de conexão com o banco de dados
        - PG_VECTOR_COLLECTION_NAME: Nome da coleção no banco de dados vetorial
        - PDF_PATH: Caminho para o arquivo ou diretório de PDFs
    
    Raises:
        EnvironmentError: Se uma ou mais variáveis de ambiente obrigatórias
                         não estiverem definidas. A mensagem de erro lista
                         todas as variáveis ausentes.
    
    Returns:
        None
    
    Examples:
        >>> validate_env_vars()  # Executa sem erro se todas as variáveis estão definidas
        
        >>> validate_env_vars()  # Levanta EnvironmentError se alguma estiver faltando
        EnvironmentError: Variáveis de ambiente ausentes: OPENAI_API_KEY, DATABASE_URL
    """
    required_vars = [
        "OPENAI_API_KEY",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
        "PDF_PATH"
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
    pass
validate_env_vars()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    template = PromptTemplate (
        input_variables=["pergunta", "contexto"],
        template=PROMPT_TEMPLATE
    )

    if (question is not None):
      most_relevant_content = search_most_relevant_content(question)  # Assume this function 
      text = template.format(pergunta=question, contexto=most_relevant_content)
      return text
    
    pass

def search_most_relevant_content(question=None, k=2):
    
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_MODEL")
    )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )
    
    results = store.similarity_search_with_score(
      query=question,
      k=k
    )
    
    # Formatar resultados como contexto para o prompt
    context_parts = []
    for i, (doc, score) in enumerate(results, start=1):
      context_parts.append(f"Documento {i} (relevância: {score:.2f}):\n{doc.page_content.strip()}")
    
    context = "\n\n---\n\n".join(context_parts)
    return context

    for i, (doc, score) in enumerate(results, start=1):
      print("="*50)
      print(f"Resultado {i} (score: {score:.2f}):")
      print("="*50)

      print("\nTexto:\n")
      print(doc.page_content.strip())

      print("\nMetadados:\n")
      for k, v in doc.metadata.items():
          print(f"{k}: {v}")

    # Lógica para buscar o conteúdo mais relevante com base na pergunta
    return "Conteúdo relevante simulado."