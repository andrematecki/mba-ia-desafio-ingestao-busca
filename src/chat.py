from search import search_prompt

def main():
    print("🤖 Chat iniciado! Digite 'sair' para encerrar.\n")

    while True:
        question = input("Você: ")

        if question.lower() in ["sair", "exit", "quit"]:
            print("\nEncerrando chat.")
            break

        prompt = search_prompt(question)
        print(f"Prompt: {prompt}\n")

    #chain = search_prompt("Aqui vai a pergunta do usuário")

    #if not chain:
    #    print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
    #    return

if __name__ == "__main__":
    main()