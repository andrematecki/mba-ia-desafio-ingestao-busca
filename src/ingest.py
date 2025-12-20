import logging
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

from helper import Helper


load_dotenv()
def get_pdf_path():
    base_dir = Path(__file__).resolve().parent
    return base_dir.parent / os.getenv("PDF_PATH")

PDF_PATH = get_pdf_path()


def ingest_pdf():
    logger = logging.getLogger(__name__)
    
    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, add_start_index=False
    )
    parts = splitter.split_documents(documents)
    logger.info("Split em chunks realizado. Número de chunks: %d", len(parts))
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
    logger.info("Enriquecimento dos chunks concluído. Total enriquecidos: %d", len(enriched_parts))
    
    ids = [f"doc-{i}" for i in range(len(enriched_parts))]
    logger.info("IDs preparados para persistência. Ex.: %s. Total de ids: %d", ids[:5], len(ids))

    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL")
    )
    logger.info("Inicializando embeddings com modelo: %s", embeddings.model)

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )
    logger.info("Instância PGVector criada (collection=%s).", os.getenv("PG_VECTOR_COLLECTION_NAME"))


    store.add_documents(documents=enriched_parts, ids=ids)
    logger.info("Persistidos %d documentos no PGVector (collection=%s).", len(enriched_parts), os.getenv("PG_VECTOR_COLLECTION_NAME"))

    logger.info("Ingestão concluída com sucesso. Total de partes criadas: %d", len(parts))

    

if __name__ == "__main__":
    Helper.configura_logging()
    Helper.valida_env_vars()
    ingest_pdf()