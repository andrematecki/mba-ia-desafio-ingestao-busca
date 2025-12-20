import os
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector  
load_dotenv()

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
      most_relevant_content = search_most_relevant_content(question, 10)  # Assume this function 
      text = template.format(pergunta=question, contexto=most_relevant_content)
      return text
    
    pass

def search_most_relevant_content(question=None, k=2):
    
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL")
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
