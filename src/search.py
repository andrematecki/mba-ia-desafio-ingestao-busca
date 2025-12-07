from langchain.prompts import PromptTemplate

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

def search_most_relevant_content(question=None, k=10):
    # Lógica para buscar o conteúdo mais relevante com base na pergunta
    return "Conteúdo relevante simulado."