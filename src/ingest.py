import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector


load_dotenv()
def get_pdf_path():
    base_dir = Path(__file__).resolve().parent
    return base_dir.parent / os.getenv("PDF_PATH")

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

def ingest_pdf():
    validate_env_vars()
    
    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, add_start_index=False
    )
    parts = splitter.split_documents(documents)
    if not parts:
        print("Nenhum chunk foi criado a partir do PDF.")
        raise SystemExit(0)

    enriched_parts = [
        Document(
            page_content=part.page_content,
            metadata={k:v for k,v in part.metadata.items() if v not in [None, ""]}  # Remove chaves com valores None ou vazios  
        )
        for part in parts
    ]
    
    ids = [f"doc-{i}" for i in range(len(enriched_parts))]


    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_MODEL")
    )

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )

    store.add_documents(documents=enriched_parts, ids=ids)

    print(f"Total de partes criadas: {len(parts)}\n")

    # for part in enriched_parts:
    #     print(part.page_content)
    #     print("-"*30)
     
PDF_PATH = get_pdf_path()

if __name__ == "__main__":
    ingest_pdf()