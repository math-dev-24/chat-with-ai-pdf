import logging
import hashlib
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.domain.ports.embedding import EmbeddingConnector
from src.domain.ports.vector import VectorConnector, Document, SearchResult
from src.tools.text_extract import PDFChapterExtractor


class VectorService:
    """Service qui orchestre la vectorisation et la recherche de documents."""

    def __init__(
            self,
            vector_adapter: VectorConnector,
            embedding_adapter: EmbeddingConnector,
    ):
        self.vector_adapter = vector_adapter
        self.embedding_adapter = embedding_adapter
        self.logger = logging.getLogger(__name__)

    def initialize(self, vector_config: Dict[str, Any], embedding_config: Dict[str, Any]) -> None:
        """
        Initialise les deux adaptateurs.

        Args:
            vector_config: Configuration pour la base vectorielle
            embedding_config: Configuration pour le générateur d'embeddings
        """
        self.logger.info("🚀 Initialisation du VectorService")

        try:
            self.embedding_adapter.initialize(embedding_config)
            self.vector_adapter.initialize(vector_config)

            if not self.vector_adapter.health_check():
                raise Exception("Health check de la base vectorielle a échoué")

            self.logger.info("✅ VectorService initialisé avec succès")

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'initialisation: {e}")
            raise

    def add_pdf_document_by_chapters(
            self,
            pdf_path: Path,
            pdf_name: Optional[str] = None
    ) -> None:
        """
        Ajoute un document PDF à la base vectorielle en le découpant par chapitres.

        Args:
            pdf_path: Chemin vers le fichier PDF
            pdf_name: Nom du fichier PDF (optionnel, utilise le nom du fichier si non fourni)
        """
        if pdf_name is None:
            pdf_name = pdf_path.name

        self.logger.info(f"📄 Ajout du document par chapitres: {pdf_name}")

        try:
            # Génération d'un ID unique pour le document
            document_id = self._generate_document_id(pdf_name, pdf_path)

            # Vérification si le document existe déjà
            if self.vector_adapter.document_exists(document_id):
                self.logger.info(f"📋 Document {pdf_name} déjà présent, suppression de l'ancien")
                self.remove_pdf_document(pdf_name, pdf_path)

            # Extraction par chapitres
            with PDFChapterExtractor(str(pdf_path)) as extractor:
                chapters = extractor.extract_chapters()

            self.logger.info(f"📚 Document découpé en {len(chapters)} chapitres")

            # Création des documents avec métadonnées
            documents = []
            for i, chapter in enumerate(chapters):
                chapter_id = f"{document_id}_chapter_{i}"

                # Préparation du contenu avec titre intégré
                content = f"# {chapter['title']}\n\n{chapter['content']}"

                doc = Document(
                    id=chapter_id,
                    content=content,
                    metadata={
                        "source_pdf": pdf_name,
                        "pdf_path": str(pdf_path),
                        "chapter_index": i,
                        "chapter_title": chapter['title'],
                        "total_chapters": len(chapters),
                        "original_document_id": document_id,
                        "content_type": "chapter",
                        "content_length": len(chapter['content'])
                    }
                )
                documents.append(doc)

            # Génération des embeddings par batch pour optimiser
            self._generate_embeddings_for_documents(documents)

            # Ajout à la base vectorielle
            self.vector_adapter.add_documents(documents)

            self.logger.info(f"✅ Document {pdf_name} ajouté avec {len(chapters)} chapitres")

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'ajout du document {pdf_name}: {e}")
            raise

    def add_pdf_document(
            self,
            pdf_name: str,
            text: str,
            pdf_path: Path,
            chunk_size: int = 1000,
            chunk_overlap: int = 200
    ) -> None:
        """
        Ajoute un document PDF à la base vectorielle en le découpant en chunks.
        (Méthode originale conservée pour compatibilité)

        Args:
            pdf_name: Nom du fichier PDF
            text: Contenu textuel du PDF
            pdf_path: Chemin vers le fichier PDF
            chunk_size: Taille des chunks en caractères
            chunk_overlap: Chevauchement entre chunks
        """
        self.logger.info(f"📄 Ajout du document par chunks: {pdf_name}")

        try:
            # Génération d'un ID unique pour le document
            document_id = self._generate_document_id(pdf_name, pdf_path)

            # Vérification si le document existe déjà
            if self.vector_adapter.document_exists(document_id):
                self.logger.info(f"📋 Document {pdf_name} déjà présent, suppression de l'ancien")
                self.vector_adapter.delete_documents([document_id])

            # Découpage du texte en chunks
            chunks = self._chunk_text(text, chunk_size, chunk_overlap)
            self.logger.info(f"✂️ Texte découpé en {len(chunks)} chunks")

            # Création des documents avec métadonnées
            documents = []
            for i, chunk in enumerate(chunks):
                chunk_id = f"{document_id}_chunk_{i}"
                doc = Document(
                    id=chunk_id,
                    content=chunk,
                    metadata={
                        "source_pdf": pdf_name,
                        "pdf_path": str(pdf_path),
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "original_document_id": document_id,
                        "content_type": "chunk"
                    }
                )
                documents.append(doc)

            # Génération des embeddings par batch pour optimiser
            self._generate_embeddings_for_documents(documents)

            # Ajout à la base vectorielle
            self.vector_adapter.add_documents(documents)

            self.logger.info(f"✅ Document {pdf_name} ajouté avec {len(chunks)} chunks")

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'ajout du document {pdf_name}: {e}")
            raise

    def search_documents(
            self,
            query: str,
            top_k: int = 5,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Recherche des documents similaires à la requête.

        Args:
            query: Requête de recherche
            top_k: Nombre de résultats à retourner
            filters: Filtres optionnels sur les métadonnées

        Returns:
            Liste des résultats de recherche
        """
        self.logger.info(f"🔍 Recherche: '{query}' (top_{top_k})")

        try:
            results = self.vector_adapter.search_similar(query, top_k, filters)
            self.logger.info(f"📊 {len(results)} résultats trouvés")
            return results

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la recherche: {e}")
            raise

    def search_by_pdf(self, query: str, pdf_name: str, top_k: int = 5) -> List[SearchResult]:
        """
        Recherche dans un PDF spécifique.

        Args:
            query: Requête de recherche
            pdf_name: Nom du PDF à cibler
            top_k: Nombre de résultats

        Returns:
            Liste des résultats de recherche
        """
        filters = {"source_pdf": pdf_name}
        return self.search_documents(query, top_k, filters)

    def search_by_chapter(self, query: str, pdf_name: str, top_k: int = 5) -> List[SearchResult]:
        """
        Recherche dans les chapitres d'un PDF spécifique.

        Args:
            query: Requête de recherche
            pdf_name: Nom du PDF à cibler
            top_k: Nombre de résultats

        Returns:
            Liste des résultats de recherche
        """
        filters = {"source_pdf": pdf_name, "content_type": "chapter"}
        return self.search_documents(query, top_k, filters)

    def get_context_for_query(
            self,
            query: str,
            max_context_length: int = 4000,
            top_k: int = 10,
            prefer_chapters: bool = True
    ) -> str:
        """
        Récupère le contexte le plus pertinent pour une requête.
        Utile pour alimenter un LLM avec du contexte.

        Args:
            query: Requête
            max_context_length: Longueur maximale du contexte
            top_k: Nombre de chunks à considérer
            prefer_chapters: Privilégier les chapitres plutôt que les chunks

        Returns:
            Contexte formaté
        """
        # Filtrer par type de contenu si demandé
        filters = {"content_type": "chapter"} if prefer_chapters else None
        results = self.search_documents(query, top_k, filters)

        # Si pas assez de résultats avec chapitres, rechercher dans tout
        if prefer_chapters and len(results) < 3:
            results = self.search_documents(query, top_k)

        context_parts = []
        current_length = 0

        for result in results:
            chunk_text = result.document.content
            source = result.document.metadata.get("source_pdf", "Unknown")

            # Ajouter titre du chapitre si disponible
            chapter_title = result.document.metadata.get("chapter_title")
            if chapter_title:
                formatted_chunk = f"[{source} - {chapter_title}]\n{chunk_text}\n"
            else:
                formatted_chunk = f"[{source}]\n{chunk_text}\n"

            if current_length + len(formatted_chunk) > max_context_length:
                break

            context_parts.append(formatted_chunk)
            current_length += len(formatted_chunk)

        return "\n---\n".join(context_parts)

    def remove_pdf_document(self, pdf_name: str, pdf_path: Path) -> None:
        """
        Supprime tous les chunks/chapitres d'un document PDF.

        Args:
            pdf_name: Nom du PDF
            pdf_path: Chemin du PDF
        """
        self.logger.info(f"🗑️ Suppression du document: {pdf_name}")

        try:
            document_id = self._generate_document_id(pdf_name, pdf_path)

            # Recherche de tous les chunks/chapitres du document
            filters = {"original_document_id": document_id}
            results = self.vector_adapter.search_similar("", top_k=1000, filters=filters)

            chunk_ids = [result.document.id for result in results]

            if chunk_ids:
                self.vector_adapter.delete_documents(chunk_ids)
                self.logger.info(f"✅ {len(chunk_ids)} éléments supprimés pour {pdf_name}")
            else:
                self.logger.info(f"📋 Aucun élément trouvé pour {pdf_name}")

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la suppression de {pdf_name}: {e}")
            raise

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur la base vectorielle.

        Returns:
            Dictionnaire avec les statistiques
        """
        try:
            total_docs = self.vector_adapter.get_document_count()
            embedding_dim = self.embedding_adapter.get_dimension()


            return {
                "total_documents": total_docs,
                "embedding_dimension": embedding_dim,
                "health_status": self.vector_adapter.health_check()
            }

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération des statistiques: {e}")
            return {"error": str(e)}

    def _generate_document_id(self, pdf_name: str, pdf_path: Path) -> str:
        """Génère un ID unique pour un document basé sur son nom et chemin."""
        content = f"{pdf_name}_{pdf_path}"
        return hashlib.md5(content.encode()).hexdigest()

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Découpe un texte en chunks avec chevauchement.

        Args:
            text: Texte à découper
            chunk_size: Taille des chunks
            overlap: Chevauchement

        Returns:
            Liste des chunks
        """
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # Si on n'est pas à la fin, essaie de couper à un espace
            if end < len(text):
                # Cherche le dernier espace dans les 100 derniers caractères
                last_space = text.rfind(' ', end - 100, end)
                if last_space > start:
                    end = last_space

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Avance avec chevauchement
            start = end - overlap

            # Évite les boucles infinies
            if start >= end:
                start = end

        return chunks

    def _generate_embeddings_for_documents(self, documents: List[Document]) -> None:
        """
        Génère les embeddings pour une liste de documents.

        Args:
            documents: Liste des documents
        """
        texts = [doc.content for doc in documents]

        try:
            # Génération par batch pour optimiser
            embeddings = self.embedding_adapter.generate_embeddings_batch(texts)

            for doc, embedding in zip(documents, embeddings):
                doc.embedding = embedding

        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la génération des embeddings: {e}")
            # Fallback: génération individuelle
            for doc in documents:
                try:
                    doc.embedding = self.embedding_adapter.generate_embedding(doc.content)
                except Exception as embedding_error:
                    self.logger.error(f"❌ Erreur embedding pour chunk: {embedding_error}")
                    raise