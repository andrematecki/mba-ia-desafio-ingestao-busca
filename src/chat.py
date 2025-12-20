import os
import sys
import logging

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from helper import Helper
from search import search_prompt

load_dotenv()

def main():
    logger = logging.getLogger(__name__)

    print("🤖 Chat iniciado! Digite 'sair' para encerrar.\n")

    while True:
        try:
            question = input("Você: ")

            if question.lower() in ["sair", "exit", "quit"]:
                print("\nEncerrando chat.")
                break

            logger.debug("Buscando prompt com `search_prompt` para a pergunta do usuário.")
            prompt = search_prompt(question)
            logger.debug("Prompt gerado/recuperado.")

            try:
                model = ChatOpenAI(model=os.getenv("OPENAI_MODEL"), temperature=0.5)
                logger.debug("Instância do modelo criada: %s", type(model).__name__)
                result = model.invoke(prompt)
                logger.debug("Resposta do modelo recebida.")
            except Exception:
                logger.exception("Erro ao invocar o modelo de chat.")
                print("Ocorreu um erro ao consultar o modelo. Verifique os logs para detalhes.")
                continue

            # Mostrar resultado ao usuário
            print(f"Assistente: {result.content}\n")
            
        except KeyboardInterrupt:
            print("\nEncerrando chat por interrupção do usuário.")
            sys.exit(0)
        except Exception:
            logger.exception("Erro inesperado no loop principal do chat.")
            print("Ocorreu um erro inesperado. Verifique os logs.")
            sys.exit(1)

if __name__ == "__main__":
    Helper.configura_logging()
    Helper.valida_env_vars()
    main()
