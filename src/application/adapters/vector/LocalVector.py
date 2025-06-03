import json
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import asdict

from src.domain.ports.vector import VectorConnector, Document, SearchResult
from src.domain.ports.embedding import EmbeddingConnector


class LocalVectorConnector(VectorConnector):
    """
    Adaptateur de base de données vectorielle locale utilisant des fichiers JSON.
    Utilise la similarité cosinus pour la recherche.
    """
    def __init__(self, embedding_connector: EmbeddingConnector):
        self.embedding_connector = embedding_connector
        self.db_path: Path|None = None
        self.documents: Dict[str, Document] = {}
        self.embeddings: Dict[str, List[float]] = {}
        self.logger = logging.getLogger(__name__)



    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialise le connecteur avec la configuration.

        Args:
            config: Configuration avec les clés:
                - db_path: Chemin vers le fichier de base de données
                - auto_save (optionnel): Sauvegarde automatique (défaut: True)
        """
        try:
            db_path = config.get("db_path")
            if not db_path:
                raise ValueError("db_path requis dans la configuration")

            self.db_path = Path(db_path)
            self.auto_save = config.get("auto_save", True)

            # Création du répertoire parent si nécessaire
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # Chargement des données existantes
            self._load_database()

            self.logger.info(f"✅ Base vectorielle locale initialisée: {self.db_path}")
            self.logger.info(f"📊 {len(self.documents)} documents chargés")

        except Exception as e:
            self.logger.error(f"❌ Erreur initialisation base vectorielle: {e}")
            raise

    def health_check(self) -> bool:
        """
        Vérifie que la base de données est accessible.

        Returns:
            True si tout va bien
        """
        try:
            # Vérification de l'accès en écriture
            test_path = self.db_path.parent / "health_check.tmp"
            test_path.write_text("test")
            test_path.unlink()

            # Vérification de la cohérence des données
            if len(self.documents) != len(self.embeddings):
                self.logger.warning("⚠️ Incohérence entre documents et embeddings")
                return False

            return True

        except Exception as e:
            self.logger.error(f"❌ Health check échoué: {e}")
            return False

    def add_documents(self, documents: List[Document]) -> None:
        """
        Ajoute des documents à la base vectorielle.

        Args:
            documents: Liste des documents à ajouter
        """
        try:
            added_count = 0

            for doc in documents:
                if not doc.embedding:
                    self.logger.warning(f"Document {doc.id} sans embedding, génération...")
                    doc.embedding = self.embedding_connector.generate_embedding(doc.content)

                # Stockage du document et de son embedding
                self.documents[doc.id] = doc
                self.embeddings[doc.id] = doc.embedding
                added_count += 1

            if self.auto_save:
                self._save_database()

            self.logger.info(f"✅ {added_count} documents ajoutés à la base vectorielle")

        except Exception as e:
            self.logger.error(f"❌ Erreur ajout documents: {e}")
            raise

    def search_similar(
            self,
            query: str,
            top_k: int = 5,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Recherche des documents similaires à la requête.

        Args:
            query: Texte de la requête
            top_k: Nombre de résultats à retourner
            filters: Filtres optionnels sur les métadonnées

        Returns:
            Liste des résultats triés par pertinence
        """
        try:
            if not self.documents:
                self.logger.info("Base de données vide")
                return []

            # Génération de l'embedding de la requête
            query_embedding = self.embedding_connector.generate_embedding(query)

            # Calcul des similarités
            similarities = []

            for doc_id, doc in self.documents.items():
                # Application des filtres
                if filters and not self._match_filters(doc, filters):
                    continue

                doc_embedding = self.embeddings[doc_id]
                similarity = self._cosine_similarity(query_embedding, doc_embedding)

                similarities.append((doc_id, similarity))

            # Tri par similarité décroissante
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Récupération des top_k résultats
            results = []
            for doc_id, score in similarities[:top_k]:
                document = self.documents[doc_id]
                result = SearchResult(document=document, score=score)
                results.append(result)

            self.logger.info(f"🔍 Recherche '{query}': {len(results)} résultats sur {len(similarities)} candidats")
            return results

        except Exception as e:
            self.logger.error(f"❌ Erreur recherche: {e}")
            raise

    def delete_documents(self, document_ids: List[str]) -> None:
        """
        Supprime des documents de la base vectorielle.

        Args:
            document_ids: Liste des IDs des documents à supprimer
        """
        try:
            deleted_count = 0

            for doc_id in document_ids:
                if doc_id in self.documents:
                    del self.documents[doc_id]
                    del self.embeddings[doc_id]
                    deleted_count += 1
                else:
                    self.logger.warning(f"Document {doc_id} non trouvé pour suppression")

            if self.auto_save and deleted_count > 0:
                self._save_database()

            self.logger.info(f"🗑️ {deleted_count} documents supprimés")

        except Exception as e:
            self.logger.error(f"❌ Erreur suppression documents: {e}")
            raise

    def get_document_count(self) -> int:
        """
        Retourne le nombre total de documents dans la base.

        Returns:
            Nombre de documents
        """
        return len(self.documents)

    def document_exists(self, document_id: str) -> bool:
        """
        Vérifie si un document existe déjà dans la base.

        Args:
            document_id: ID du document à vérifier

        Returns:
            True si le document existe
        """
        return document_id in self.documents

    def save_database(self) -> None:
        """Force la sauvegarde de la base de données."""
        self._save_database()

    def optimize_database(self) -> None:
        """
        Optimise la base de données (nettoyage, réindexation).
        Pour cette implémentation simple, vérifie juste la cohérence.
        """
        try:
            # Nettoyage des embeddings orphelins
            orphaned_embeddings = set(self.embeddings.keys()) - set(self.documents.keys())
            for orphan_id in orphaned_embeddings:
                del self.embeddings[orphan_id]

            # Régénération des embeddings manquants
            missing_embeddings = set(self.documents.keys()) - set(self.embeddings.keys())
            for doc_id in missing_embeddings:
                doc = self.documents[doc_id]
                self.embeddings[doc_id] = self.embedding_connector.generate_embedding(doc.content)

            if self.auto_save and (orphaned_embeddings or missing_embeddings):
                self._save_database()

            self.logger.info(
                f"🔧 Optimisation: {len(orphaned_embeddings)} orphelins supprimés, {len(missing_embeddings)} embeddings régénérés")

        except Exception as e:
            self.logger.error(f"❌ Erreur optimisation: {e}")
            raise

    def _load_database(self) -> None:
        """Charge la base de données depuis le fichier."""
        try:
            if not self.db_path.exists():
                self.logger.info("Nouveau fichier de base de données")
                self.documents = {}
                self.embeddings = {}
                return

            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Reconstruction des documents
            self.documents = {}
            for doc_data in data.get('documents', []):
                doc = Document(
                    id=doc_data['id'],
                    content=doc_data['content'],
                    metadata=doc_data['metadata'],
                    embedding=doc_data.get('embedding')
                )
                self.documents[doc.id] = doc

            # Chargement des embeddings
            self.embeddings = data.get('embeddings', {})

            self.logger.info(f"📂 Base de données chargée: {len(self.documents)} documents")

        except Exception as e:
            self.logger.error(f"❌ Erreur chargement base: {e}")
            # Initialisation vide en cas d'erreur
            self.documents = {}
            self.embeddings = {}

    def _save_database(self) -> None:
        """Sauvegarde la base de données dans le fichier."""
        try:
            # Préparation des données pour la sérialisation
            documents_data = []
            for doc in self.documents.values():
                doc_dict = asdict(doc)
                documents_data.append(doc_dict)

            data = {
                'documents': documents_data,
                'embeddings': self.embeddings,
                'metadata': {
                    'version': '1.0',
                    'document_count': len(self.documents),
                    'embedding_dimension': len(next(iter(self.embeddings.values()))) if self.embeddings else 0
                }
            }

            # Sauvegarde atomique (fichier temporaire puis renommage)
            temp_path = self.db_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            temp_path.replace(self.db_path)

            self.logger.debug(f"💾 Base de données sauvegardée: {self.db_path}")

        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde base: {e}")
            raise

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcule la similarité cosinus entre deux vecteurs.

        Args:
            vec1: Premier vecteur
            vec2: Deuxième vecteur

        Returns:
            Similarité cosinus (0 à 1)
        """
        try:
            # Conversion en arrays numpy pour l'efficacité
            a = np.array(vec1)
            b = np.array(vec2)

            # Calcul de la similarité cosinus
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)

            if norm_a == 0 or norm_b == 0:
                return 0.0

            similarity = dot_product / (norm_a * norm_b)

            # Conversion en score positif (0 à 1)
            return (similarity + 1) / 2

        except Exception as e:
            self.logger.error(f"❌ Erreur calcul similarité: {e}")
            return 0.0

    def _match_filters(self, document: Document, filters: Dict[str, Any]) -> bool:
        """
        Vérifie si un document correspond aux filtres.

        Args:
            document: Document à vérifier
            filters: Filtres à appliquer

        Returns:
            True si le document correspond
        """
        for key, value in filters.items():
            if key not in document.metadata:
                return False

            doc_value = document.metadata[key]

            # Correspondance exacte
            if doc_value != value:
                return False

        return True