import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from search import search_prompt
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


def main():
    print("🤖 Chat iniciado! Digite 'sair' para encerrar.\n")

    while True:
        question = input("Você: ")

        if question.lower() in ["sair", "exit", "quit"]:
            print("\nEncerrando chat.")
            break

        prompt = search_prompt(question)


        model = ChatOpenAI(model="gpt-5-mini", temperature=0.5)
        result = model.invoke(prompt)
        print(f"Assistente: {result.content}\n")
     
        


        #print(f"Prompt: {prompt}\n")

    #chain = search_prompt("Aqui vai a pergunta do usuário")

    #if not chain:
    #    print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
    #    return

if __name__ == "__main__":
    main()