import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict, Any, Union
import logging
import time
from src.tools.document_processor import DocumentProcessor


class VectorStore:
    """Service de base vectorielle avec support LangChain"""

    def __init__(self, collection_name: str = "documents", persist_directory: str = "./chroma_db"):
        """
        Initialise le VectorStore

        Args:
            collection_name: Nom de la collection Chroma
            persist_directory: Répertoire de persistance
        """
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)

        # Modèle d'embedding (gardez votre modèle actuel ou changez)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Nouveau processeur de documents avec LangChain
        self.document_processor = DocumentProcessor(
            chunk_size=1000,
            chunk_overlap=200
        )

        logging.info(f"VectorStore initialisé avec collection '{collection_name}'")

    def add_documents_from_files(self, file_paths: List[Union[Path, str]]) -> Dict[str, Any]:
        """
        MÉTHODE MISE À JOUR: Ajoute des documents via LangChain
        Compatible avec votre code existant

        Args:
            file_paths: Liste des chemins de fichiers (Path objects ou strings)

        Returns:
            Statistiques du traitement
        """
        # Conversion en Path objects si nécessaire
        path_objects = []
        for fp in file_paths:
            if isinstance(fp, str):
                path_objects.append(Path(fp))
            else:
                path_objects.append(fp)

        logging.info(f"🚀 Traitement de {len(path_objects)} fichier(s) avec LangChain...")

        # Traitement avec LangChain
        chunks = self.document_processor.process_files(path_objects)

        if not chunks:
            logging.warning("Aucun chunk à traiter")
            return {
                'total_chunks': 0,
                'total_files': 0,
                'files_processed': []
            }

        # Ajout à la collection
        self._add_chunks_to_collection(chunks)

        # Statistiques
        stats = self.document_processor.get_chunk_info(chunks)
        logging.info(f"✅ Terminé! {stats}")

        return stats

    def _add_chunks_to_collection(self, chunks: List) -> None:
        """
        Méthode interne pour ajouter des chunks à la collection

        Args:
            chunks: Liste des chunks LangChain
        """
        # Préparation des données pour Chroma avec IDs uniques
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        # Génération d'IDs uniques pour éviter les conflits
        timestamp = int(time.time())
        ids = [f"{chunk.metadata['source_file']}_{chunk.metadata['chunk_id']}_{timestamp}_{idx}"
               for idx, chunk in enumerate(chunks)]

        # Vectorisation
        logging.info(f"🔄 Vectorisation de {len(texts)} chunks...")
        embeddings = self.embedding_model.encode(texts).tolist()

        # Ajout à Chroma avec gestion robuste des gros volumes
        batch_size = 50  # Réduit pour éviter les timeouts
        total_batches = (len(texts) + batch_size - 1) // batch_size

        logging.info(f"💾 Ajout en {total_batches} batch(s) de {batch_size} chunks...")

        for i in range(0, len(texts), batch_size):
            batch_num = i // batch_size + 1
            batch_texts = texts[i:i+batch_size]
            batch_embeddings = embeddings[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]

            try:
                # Nettoyage des métadonnées pour éviter les caractères problématiques
                clean_metadatas = []
                for metadata in batch_metadatas:
                    clean_metadata = {}
                    for key, value in metadata.items():
                        if isinstance(value, str):
                            # Nettoie les caractères Unicode problématiques
                            clean_value = value.encode('utf-8', 'ignore').decode('utf-8')
                            clean_metadata[key] = clean_value
                        else:
                            clean_metadata[key] = value
                    clean_metadatas.append(clean_metadata)

                self.collection.add(
                    documents=batch_texts,
                    embeddings=batch_embeddings,
                    metadatas=clean_metadatas,
                    ids=batch_ids
                )

                if batch_num % 10 == 0 or batch_num == total_batches:
                    logging.info(f"   📊 Batch {batch_num}/{total_batches} ajouté ({len(batch_texts)} chunks)")

            except Exception as e:
                logging.error(f"❌ Erreur batch {batch_num}: {e}")
                # Continue avec le batch suivant plutôt que d'échouer complètement
                continue

    def get_context_for_query(self, query: str, max_context_length: int = 4000, n_results: int = 5) -> str:
        """
        Args:
            query: Question de l'utilisateur
            max_context_length: Longueur max du contexte
            prefer_chapters: Préférence pour les chapitres (peut être ignoré pour l'instant)
            n_results: Nombre de résultats à récupérer

        Returns:
            Contexte formaté pour le LLM
        """
        try:
            query_embedding = self.embedding_model.encode([query]).tolist()

            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )

            if not results["documents"] or not results["documents"][0]:
                return "Aucun contexte trouvé."

            context_parts = []
            current_length = 0

            documents = results["documents"][0]
            metadatas = results["metadatas"][0] if results["metadatas"] else []
            distances = results["distances"][0] if results["distances"] else []

            for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                if current_length + len(doc) > max_context_length:
                    break

                source_info = ""
                if metadata:
                    source_file = metadata.get('source_file', 'Unknown')
                    page_info = metadata.get('page', '')
                    if page_info:
                        source_info = f"[Source: {source_file}, Page: {page_info}]"
                    else:
                        source_info = f"[Source: {source_file}]"

                context_part = f"{source_info}\n{doc}\n---"
                context_parts.append(context_part)
                current_length += len(context_part)

            context = "\n".join(context_parts)

            logging.info(f"🔍 Contexte généré: {len(context)} caractères, {len(context_parts)} sources")
            return context

        except Exception as e:
            logging.error(f"❌ Erreur lors de la recherche: {e}")
            return f"Erreur lors de la recherche: {str(e)}"

    def search_with_metadata(self, query: str, n_results: int = 5, file_filter: str = None) -> Dict[str, Any]:
        """
        Args:
            query: Requête de recherche
            n_results: Nombre de résultats
            file_filter: Filtrer par nom de fichier

        Returns:
            Résultats de la recherche
        """
        try:
            query_embedding = self.embedding_model.encode([query]).tolist()

            # Filtrage optionnel par fichier
            where_clause = {}
            if file_filter:
                where_clause["source_file"] = {"$eq": file_filter}

            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                where=where_clause if where_clause else None,
                include=["documents", "metadatas", "distances"]
            )

            return results
        except Exception as e:
            logging.error(f"❌ Erreur recherche avec métadonnées: {e}")
            return {"error": str(e)}

    def get_file_list(self) -> List[str]:
        try:
            all_data = self.collection.get(include=["metadatas"])
            files = set()
            for metadata in all_data["metadatas"]:
                if metadata and "source_file" in metadata:
                    files.add(metadata["source_file"])
            return sorted(list(files))
        except Exception as e:
            logging.error(f"❌ Erreur récupération liste fichiers: {e}")
            return []

    def get_collection_stats(self) -> Dict[str, Any]:
        try:
            count = self.collection.count()
            files = self.get_file_list()

            return {
                "total_chunks": count,
                "total_files": len(files),
                "files": files
            }
        except Exception as e:
            logging.error(f"❌ Erreur statistiques collection: {e}")
            return {
                "total_chunks": 0,
                "total_files": 0,
                "files": [],
                "error": str(e)
            }

    def clear_collection(self) -> bool:
        try:
            # Supprime et recrée la collection
            collection_name = self.collection.name
            self.client.delete_collection(collection_name)
            self.collection = self.client.create_collection(collection_name)
            logging.info("🗑️ Collection vidée avec succès")
            return True
        except Exception as e:
            logging.error(f"❌ Erreur lors du vidage: {e}")
            return False

    def get_collection_size(self) -> int:
        try:
            return self.collection.count()
        except Exception as e:
            logging.error(f"❌ Erreur lors du comptage: {e}")
            return 0

    def delete_file_chunks(self, file_name: str) -> bool:
        """
        Args:
            file_name: Nom du fichier à supprimer

        Returns:
            True si succès
        """
        try:
            results = self.collection.get(
                where={"source_file": {"$eq": file_name}},
                include=["metadatas"]
            )

            if results["ids"]:
                self.collection.delete(ids=results["ids"])
                logging.info(f"🗑️ Supprimé {len(results['ids'])} chunks du fichier {file_name}")
                return True
            else:
                logging.info(f"Aucun chunk trouvé pour le fichier {file_name}")
                return True

        except Exception as e:
            logging.error(f"❌ Erreur suppression fichier {file_name}: {e}")
            return False