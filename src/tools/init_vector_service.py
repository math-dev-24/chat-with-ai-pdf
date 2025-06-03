import os, logging
from pathlib import Path
from dotenv import load_dotenv
from src.application.adapters.embedding.OpenAI import OpenAiEmbeddingConnector
from src.application.adapters.vector.LocalVector import LocalVectorConnector
from src.domain.services.vector_service import VectorService


def initialize_vector_service() -> VectorService:
    """
    Initialise le service de vectorisation.

    Returns:
        Service de vectorisation configuré
    """
    load_dotenv()

    VECTOR_DB_PATH = Path(os.getenv("VECTOR_DB_PATH", "data/vector_db.json"))

    try:
        embedding_config = {
            "model": "text-embedding-3-small",
            "dimension": 1536
        }

        vector_config = {
            "db_path": str(VECTOR_DB_PATH),
            "auto_save": True
        }

        # Création des adaptateurs
        embedding_connector = OpenAiEmbeddingConnector()
        vector_connector = LocalVectorConnector(embedding_connector)

        # Création du service
        vector_service = VectorService(vector_connector, embedding_connector)
        vector_service.initialize(vector_config, embedding_config)

        return vector_service

    except Exception as e:
        logging.error(f"❌ Erreur initialisation VectorService: {e}")
        raise