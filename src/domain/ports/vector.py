from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Document:
    """Représente un document avec son contenu et métadonnées."""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


@dataclass
class SearchResult:
    """Résultat d'une recherche vectorielle."""
    document: Document
    score: float


class VectorConnector(ABC):
    """Interface abstraite pour les connecteurs de base de données vectorielles."""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialise le connecteur avec la configuration spécifique.

        Args:
            config: Configuration spécifique au fournisseur (chemin DB, dimensions, etc.)
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Vérifie que la connexion à la base vectorielle fonctionne.

        Returns:
            True si la connexion est OK
        """
        pass

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """
        Ajoute des documents à la base vectorielle.

        Args:
            documents: Liste des documents à ajouter
        """
        pass

    @abstractmethod
    def search_similar(self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[
        SearchResult]:
        """
        Recherche des documents similaires à la requête.

        Args:
            query: Texte de la requête
            top_k: Nombre de résultats à retourner
            filters: Filtres optionnels sur les métadonnées

        Returns:
            Liste des résultats triés par pertinence
        """
        pass

    @abstractmethod
    def delete_documents(self, document_ids: List[str]) -> None:
        """
        Supprime des documents de la base vectorielle.

        Args:
            document_ids: Liste des IDs des documents à supprimer
        """
        pass

    @abstractmethod
    def get_document_count(self) -> int:
        """
        Retourne le nombre total de documents dans la base.

        Returns:
            Nombre de documents
        """
        pass

    @abstractmethod
    def document_exists(self, document_id: str) -> bool:
        """
        Vérifie si un document existe déjà dans la base.

        Args:
            document_id: ID du document à vérifier

        Returns:
            True si le document existe
        """
        pass