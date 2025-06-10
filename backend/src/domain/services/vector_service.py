import chromadb
from pathlib import Path
from typing import List, Dict, Any, Union
import logging
import time
from src.tools.document_processor import DocumentProcessor
from src.domain.ports.embeding import EmbeddingPort


class VectorStore:
    """Service de base vectorielle avec support LangChain"""

    def __init__(self, 
                 embedding_port: EmbeddingPort,
                 collection_name: str = "documents", 
                 persist_directory: str = "./chroma_db"):
        """
        Initialise le VectorStore

        Args:
            embedding_port: Port d'embedding à utiliser
            collection_name: Nom de la collection Chroma
            persist_directory: Répertoire de persistance
        """
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedding_port = embedding_port

        self.document_processor = DocumentProcessor(
            chunk_size=1000,
            chunk_overlap=200
        )

        logging.info(f"VectorStore initialisé avec collection '{collection_name}' et modèle '{embedding_port.get_model_name()}'")

    def add_documents_from_files(self, file_paths: List[Union[Path, str]], user_id: str) -> Dict[str, Any]:
        """
        MÉTHODE MISE À JOUR: Ajoute des documents via LangChain
        Compatible avec votre code existant

        Args:
            file_paths: Liste des chemins de fichiers (Path objects ou strings)
            user_id: ID unique de l'utilisateur

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

        # Ajout à la collection avec l'ID utilisateur
        self._add_chunks_to_collection(chunks, user_id)

        # Statistiques
        stats = self.document_processor.get_chunk_info(chunks)
        logging.info(f"✅ Terminé! {stats}")

        return stats

    def _add_chunks_to_collection(self, chunks: List, user_id: str) -> None:
        """
        Méthode interne pour ajouter des chunks à la collection

        Args:
            chunks: Liste des chunks LangChain
            user_id: ID unique de l'utilisateur
        """
        # Préparation des données pour Chroma avec IDs uniques
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        # Ajout de l'ID utilisateur aux métadonnées
        for metadata in metadatas:
            metadata['user_id'] = user_id

        # Génération d'IDs uniques pour éviter les conflits
        timestamp = int(time.time())
        ids = [f"{user_id}_{chunk.metadata['source_file']}_{chunk.metadata['chunk_id']}_{timestamp}_{idx}"
               for idx, chunk in enumerate(chunks)]

        # Vectorisation via le port d'embedding
        logging.info(f"🔄 Vectorisation de {len(texts)} chunks...")
        embeddings = self.embedding_port.encode(texts)

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

    def get_context_for_query(self, query: str, user_id: str, max_context_length: int = 4000, n_results: int = 5) -> dict:
        """
        Args:
            query: Question de l'utilisateur
            user_id: ID unique de l'utilisateur
            max_context_length: Longueur max du contexte
            n_results: Nombre de résultats à récupérer

        Returns:
            Dictionnaire contenant:
            - context: Contexte formaté pour le LLM
            - sources: Liste des sources utilisées
        """
        try:
            query_embedding = self.embedding_port.encode([query])

            where_clause = {"user_id": {"$eq": user_id}}

            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )

            if not results["documents"] or not results["documents"][0]:
                return {
                    "context": "Aucun contexte trouvé.",
                    "sources": []
                }

            context_parts = []
            sources = set()
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
                    sources.add(source_file)
                    if page_info:
                        source_info = f"[Source: {source_file}, Page: {page_info}]"
                    else:
                        source_info = f"[Source: {source_file}]"

                context_part = f"{source_info}\n{doc}\n---"
                context_parts.append(context_part)
                current_length += len(context_part)

            context = "\n".join(context_parts)

            logging.info(f"🔍 Contexte généré: {len(context)} caractères, {len(context_parts)} sources")
            return {
                "context": context,
                "sources": list(sources)
            }

        except Exception as e:
            logging.error(f"❌ Erreur lors de la recherche: {e}")
            return {
                "context": f"Erreur lors de la recherche: {str(e)}",
                "sources": []
            }

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
            query_embedding = self.embedding_port.encode([query])

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

    def get_file_list(self, user_id: str) -> List[str]:
        try:
            # Filtre par utilisateur
            where_clause = {"user_id": {"$eq": user_id}}
            all_data = self.collection.get(where=where_clause, include=["metadatas"])
            files = set()
            for metadata in all_data["metadatas"]:
                if metadata and "source_file" in metadata:
                    files.add(metadata["source_file"])
            return sorted(list(files))
        except Exception as e:
            logging.error(f"❌ Erreur récupération liste fichiers: {e}")
            return []

    def get_collection_stats(self, user_id: str) -> Dict[str, Any]:
        try:
            where_clause = {"user_id": {"$eq": user_id}}
            results = self.collection.get(where=where_clause)
            count = len(results["ids"]) if results["ids"] else 0
            files = self.get_file_list(user_id)

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

    def clear_collection(self, user_id: str) -> bool:
        try:
            # Supprime uniquement les documents de l'utilisateur
            where_clause = {"user_id": {"$eq": user_id}}
            results = self.collection.get(where=where_clause)
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
            logging.info(f"🗑️ Documents de l'utilisateur {user_id} supprimés avec succès")
            return True
        except Exception as e:
            logging.error(f"❌ Erreur lors du vidage: {e}")
            return False

    def get_collection_size(self, user_id: str) -> int:
        try:
            where_clause = {"user_id": {"$eq": user_id}}
            results = self.collection.get(where=where_clause)
            return len(results["ids"]) if results["ids"] else 0
        except Exception as e:
            logging.error(f"❌ Erreur lors du comptage: {e}")
            return 0

    def delete_file_chunks(self, file_name: str, user_id: str) -> bool:
        """
        Args:
            file_name: Nom du fichier à supprimer
            user_id: ID unique de l'utilisateur

        Returns:
            True si succès
        """
        try:
            where_clause = {
                "$and": [
                    {"source_file": {"$eq": file_name}},
                    {"user_id": {"$eq": user_id}}
                ]
            }
            
            results = self.collection.get(
                where=where_clause,
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