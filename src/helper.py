import os
import logging

class Helper:
    @staticmethod
    def configura_logging():
        """
        Configura logging básico a partir da variável de ambiente LOG_LEVEL.

        Args:
            default_level: nível padrão se LOG_LEVEL não estiver definido.
            name: nome do logger a ser retornado. Se None, retorna o logger raiz.

        Returns:
            logging.Logger: logger configurado.
        """
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        numeric_level = getattr(logging, log_level, logging.INFO)
        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        for lib in ("httpx", "urllib3", "openai", "langchain", "httpcore"):
            logging.getLogger(lib).setLevel(logging.ERROR)
    

    @staticmethod  
    def valida_env_vars():

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
        logger = logging.getLogger(__name__)

        required_vars = [
            "OPENAI_API_KEY",
            "DATABASE_URL",
            "PG_VECTOR_COLLECTION_NAME",
            "PDF_PATH",
            "LOG_LEVEL"
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.error("Variáveis de ambiente ausentes: %s", ", ".join(missing_vars))
            raise EnvironmentError(f"Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
        logger.debug("Todas as variáveis de ambiente obrigatórias estão definidas.")
