from typing import List, Dict, Any
from pathlib import Path
import hashlib
import re
from datetime import datetime

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class DocumentProcessor:
    """Processeur de documents ultra-robuste avec LangChain"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor

        Args:
            chunk_size: Taille des chunks en caractères
            chunk_overlap: Chevauchement entre chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Splitter intelligent qui respecte la structure du texte
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",  # Paragraphes
                "\n",  # Lignes
                ".",  # Phrases
                "!",  # Exclamations
                "?",  # Questions
                ";",  # Points-virgules
                ",",  # Virgules
                " ",  # Espaces
                ""  # Caractères
            ],
            length_function=len,
        )

        # Mapping des extensions vers les loaders
        self.loaders = {
            '.pdf': PyPDFLoader,
            '.docx': UnstructuredWordDocumentLoader,
            '.doc': UnstructuredWordDocumentLoader,
            '.txt': TextLoader,
        }

    def _detect_file_type(self, file_path: Path) -> str:
        file_name = file_path.name.lower().strip()

        file_name = re.sub(r'[^\w\s.-]', '', file_name)

        print(f"  🔍 Analyse du fichier: '{file_path.name}'")
        print(f"     Nom nettoyé: '{file_name}'")

        for extension in self.loaders.keys():
            if file_name.endswith(extension):
                print(f"     ✅ Extension détectée: {extension}")
                return extension

            if extension == '.pdf' and file_name.endswith('pdf'):
                print(f"     ✅ Extension PDF détectée (variante)")
                return '.pdf'

        pathlib_ext = file_path.suffix.lower().strip()
        if pathlib_ext in self.loaders:
            print(f"     ✅ Extension via pathlib: {pathlib_ext}")
            return pathlib_ext

        if '.pdf' in file_name or file_name.endswith('pdf'):
            print(f"     ✅ PDF détecté par pattern")
            return '.pdf'

        raise ValueError(f"❌ Type de fichier non supporté pour: '{file_path.name}'\n"
                         f"   Extension brute: '{file_path.suffix}'\n"
                         f"   Nom nettoyé: '{file_name}'")

    def load_document(self, file_path: Path) -> List[Document]:
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

        try:
            extension = self._detect_file_type(file_path)
        except ValueError as e:
            print(f"     ⚠️  {e}")
            raise

        loader_class = self.loaders[extension]

        try:
            print(f"     🔄 Chargement avec {loader_class.__name__}...")

            file_path_str = str(file_path).replace('\\', '/')

            if extension == '.txt':
                loader = loader_class(file_path_str, encoding='utf-8')
            else:
                loader = loader_class(file_path_str)

            documents = loader.load()
            print(f"     ✅ {len(documents)} page(s) chargée(s)")

            for doc in documents:
                doc.metadata.update({
                    'source_file': file_path.name,
                    'source_path': str(file_path.absolute()),
                    'file_type': extension,
                    'file_size': file_path.stat().st_size,
                    'processed_at': datetime.now().isoformat(),
                    'file_hash': self._get_file_hash(file_path)
                })

            return documents

        except Exception as e:
            print(f"     ❌ Erreur de chargement: {e}")
            raise Exception(f"Erreur lors du chargement de {file_path.name}: {str(e)}")

    def split_documents(self, documents: List[Document]) -> List[Document]:
        if not documents:
            return []

        chunks = self.text_splitter.split_documents(documents)

        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                'chunk_id': i,
                'chunk_size': len(chunk.page_content),
                'chunk_hash': hashlib.md5(chunk.page_content.encode()).hexdigest()
            })

        return chunks

    def process_file(self, file_path: Path) -> List[Document]:
        print(f"📄 Traitement de {file_path.name}...")

        try:
            documents = self.load_document(file_path)

            if not documents:
                print(f"     ⚠️  Aucun contenu extrait")
                return []

            chunks = self.split_documents(documents)
            print(f"     ✅ {len(chunks)} chunk(s) créé(s)")

            return chunks

        except Exception as e:
            print(f"     ❌ Échec du traitement: {e}")
            return []

    def process_files(self, file_paths: List[Path]) -> List[Document]:
        all_chunks = []
        successful_files = 0

        for file_path in file_paths:
            chunks = self.process_file(file_path)
            if chunks:
                all_chunks.extend(chunks)
                successful_files += 1

        print(
            f"🎉 Résumé: {len(all_chunks)} chunks de {successful_files}/{len(file_paths)} fichiers traités avec succès")
        return all_chunks

    def _get_file_hash(self, file_path: Path) -> str:
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return "hash_error"

    def get_chunk_info(self, chunks: List[Document]) -> Dict[str, Any]:
        if not chunks:
            return {
                'total_chunks': 0,
                'total_files': 0,
                'files_processed': []
            }

        sizes = [len(chunk.page_content) for chunk in chunks]
        files = set(chunk.metadata['source_file'] for chunk in chunks)

        return {
            'total_chunks': len(chunks),
            'total_files': len(files),
            'avg_chunk_size': sum(sizes) / len(sizes),
            'min_chunk_size': min(sizes),
            'max_chunk_size': max(sizes),
            'total_characters': sum(sizes),
            'files_processed': list(files)
        }