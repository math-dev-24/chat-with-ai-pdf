import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

from src.domain.ports.embedding import EmbeddingConnector


class OpenAiEmbeddingConnector(EmbeddingConnector):
    """Adaptateur OpenAI pour la génération d'embeddings."""

    def __init__(self):
        self.client: OpenAI|None = None
        self.model: str = "text-embedding-3-small"
        self.dimension: int = 1536
        self.logger = logging.getLogger(__name__)

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialise le connecteur OpenAI.

        Args:
            config: Configuration avec les clés:
                - model (optionnel): Modèle d'embedding à utiliser
                - dimension (optionnel): Dimension des embeddings
        """
        load_dotenv()

        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logging.error("OpenAI API key n'existe pas")
                raise ValueError("OPENAI_API_KEY non trouvée dans les variables d'environnement")

            self.client = OpenAI(api_key=api_key)

            self.model = config.get("model", "text-embedding-3-small")

            model_dimensions = {
                "text-embedding-3-small": 1536,
                "text-embedding-3-large": 3072,
                "text-embedding-ada-002": 1536
            }

            self.dimension = config.get("dimension", model_dimensions.get(self.model, 1536))

            self._test_connection()

            self.logger.info(f"✅ OpenAI Embedding initialisé - Modèle: {self.model}, Dimension: {self.dimension}")

        except Exception as e:
            self.logger.error(f"❌ Erreur initialisation OpenAI Embedding: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """
        Génère un embedding pour un texte donné.

        Args:
            text: Texte à vectoriser

        Returns:
            Vecteur d'embedding
        """
        if not self.client:
            raise RuntimeError("Connecteur non initialisé. Appelez initialize() d'abord.")

        if not text or not text.strip():
            self.logger.warning("Texte vide pour l'embedding, retour d'un vecteur zéro")
            return [0.0] * self.dimension

        try:
            # Nettoyage du texte
            cleaned_text = self._clean_text(text)

            response = self.client.embeddings.create(
                model=self.model,
                input=cleaned_text,
                dimensions=self.dimension if self.model.startswith("text-embedding-3") else None
            )

            embedding = response.data[0].embedding

            self.logger.debug(f"Embedding généré pour texte de {len(text)} caractères")
            return embedding

        except Exception as e:
            self.logger.error(f"❌ Erreur génération embedding: {e}")
            raise

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Génère des embeddings pour une liste de textes (plus efficace).

        Args:
            texts: Liste des textes à vectoriser

        Returns:
            Liste des vecteurs d'embedding
        """
        if not self.client:
            raise RuntimeError("Connecteur non initialisé. Appelez initialize() d'abord.")

        if not texts:
            return []

        try:
            # Nettoyage des textes
            cleaned_texts = [self._clean_text(text) for text in texts]

            # Filtrage des textes vides
            valid_texts = []
            empty_indices = []

            for i, text in enumerate(cleaned_texts):
                if text and text.strip():
                    valid_texts.append(text)
                else:
                    empty_indices.append(i)

            if not valid_texts:
                self.logger.warning("Tous les textes sont vides, retour de vecteurs zéro")
                return [[0.0] * self.dimension] * len(texts)

            # Traitement par batch (OpenAI limite à ~2048 inputs)
            batch_size = 100  # Taille de batch conservative
            all_embeddings = []

            for i in range(0, len(valid_texts), batch_size):
                batch = valid_texts[i:i + batch_size]

                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    dimensions=self.dimension if self.model.startswith("text-embedding-3") else None
                )

                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)

            # Reconstruction avec les textes vides
            result_embeddings = []
            valid_idx = 0

            for i in range(len(texts)):
                if i in empty_indices:
                    result_embeddings.append([0.0] * self.dimension)
                else:
                    result_embeddings.append(all_embeddings[valid_idx])
                    valid_idx += 1

            self.logger.info(f"✅ {len(texts)} embeddings générés en batch")
            return result_embeddings

        except Exception as e:
            self.logger.error(f"❌ Erreur génération embeddings batch: {e}")
            raise

    def get_dimension(self) -> int:
        """
        Retourne la dimension des embeddings générés.

        Returns:
            Dimension du vecteur
        """
        return self.dimension

    def _clean_text(self, text: str) -> str:
        """
        Nettoie le texte avant embedding.

        Args:
            text: Texte à nettoyer

        Returns:
            Texte nettoyé
        """
        if not text:
            return ""

        # Suppression des caractères de contrôle et normalisation
        cleaned = text.strip()
        cleaned = ' '.join(cleaned.split())  # Normalise les espaces

        # Limitation de la taille (OpenAI a une limite)
        max_length = 8000  # Limite conservative
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length]
            self.logger.warning(f"Texte tronqué à {max_length} caractères")

        return cleaned

    def _test_connection(self) -> None:
        """Test la connexion avec OpenAI."""
        try:
            test_response = self.client.embeddings.create(
                model=self.model,
                input="test connection",
                dimensions=self.dimension if self.model.startswith("text-embedding-3") else None
            )

            if not test_response.data or len(test_response.data[0].embedding) != self.dimension:
                raise RuntimeError("Réponse OpenAI invalide lors du test")

        except Exception as e:
            raise RuntimeError(f"Test de connexion OpenAI échoué: {e}")

    def get_cost_estimation(self, total_tokens: int) -> float:
        """
        Estime le coût pour un nombre de tokens donné.

        Args:
            total_tokens: Nombre total de tokens

        Returns:
            Coût estimé en USD
        """
        # Prix par 1000 tokens (à jour au moment de l'implémentation)
        pricing = {
            "text-embedding-3-small": 0.00002,  # $0.02 / 1M tokens
            "text-embedding-3-large": 0.00013,  # $0.13 / 1M tokens  
            "text-embedding-ada-002": 0.0001  # $0.10 / 1M tokens
        }

        price_per_1k = pricing.get(self.model, 0.0001)
        return (total_tokens / 1000) * price_per_1k