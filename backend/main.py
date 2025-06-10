import logging, os
import time
# ______________________________________________________________________________________________________________________
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
# ______________________________________________________________________________________________________________________
from src.application.adapters.ai_chat.openAI import OpenAiConnector
from src.application.adapters.embeding.localEmbeding import LocalEmbeddingAdapter
from src.domain.services.ai_service import AiService
from src.api.schemas.chat_input import AskDataInput
from src.api.schemas.chat_response import AskDataResponse
from src.api.schemas.history import HistoryMessage
from src.domain.services.vector_service import VectorStore
from src.tools.file import get_pdf_files
from src.api.schemas.pdf_input import LoadAllPdfInput, ProcessPdfByFileInput, DeleteFileInput
# ______________________________________________________________________________________________________________________
load_dotenv()
# ______________________________________________________________________________________________________________________
PDF_PATH = Path(os.getenv("PDF_PATH"))
EXTENSIONS: list[str] = ["pdf"]
# ______________________________________________________________________________________________________________________
app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_service = AiService(OpenAiConnector())
vector_store = VectorStore(LocalEmbeddingAdapter())

@app.get("/stat")
def get_stat(user_id: str):
    return vector_store.get_collection_stats(user_id)

@app.post("/ask", response_model=AskDataResponse)
def ask(data: AskDataInput):
    try:
        start_time = time.time()

        context_result = vector_store.get_context_for_query(
            query=data.question,
            user_id=data.user_id,
            max_context_length=data.max_context_length
        )

        history_context = data.get_formatted_history()

        ai_response = ai_service.response(
            question=data.question,
            context=context_result["context"],
            history=history_context
        )

        updated_history = data.historics.copy()
        updated_history.append(HistoryMessage(role="user", content=data.question))
        updated_history.append(HistoryMessage(role="assistant", content=ai_response))

        processing_time = time.time() - start_time

        return AskDataResponse(
            question=data.question,
            response=ai_response,
            context=context_result["context"],
            context_length=len(context_result["context"]),
            sources_count=len(context_result["sources"]),
            sources=context_result["sources"],
            processing_time=processing_time,
            updated_history=updated_history
        )

    except Exception as e:
        logging.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pdfs/process-all")
def process_all_pdfs(data: LoadAllPdfInput):
    """Traite tous les PDFs du dossier configuré avec limitation
    
    Args:
        user_id: ID unique de l'utilisateur
        custom_pdf_path (str, optional): Chemin personnalisé vers le dossier contenant les PDFs
    """
    chunk_limit = 1000

    try:
        user_id = data.user_id

        if not user_id:
            raise HTTPException(status_code=400, detail="user_id est requis")

        custom_pdf_path = data.custom_pdf_path

        pdf_path = Path(custom_pdf_path) if custom_pdf_path else PDF_PATH

        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="Dossier PDF non trouvé")

        list_pdf: List[Path] = get_pdf_files(pdf_path, EXTENSIONS)

        all_chunks = []
        for pdf_file in list_pdf:
            if len(all_chunks) >= chunk_limit:
                logging.info(f"Limite de {chunk_limit} chunks atteinte")
                break

            try:
                file_chunks = vector_store.document_processor.process_file(pdf_file)
                remaining_space = chunk_limit - len(all_chunks)
                all_chunks.extend(file_chunks[:remaining_space])
            except Exception as e:
                logging.error(f"Erreur avec {pdf_file}: {e}")
                continue

        if all_chunks:
            vector_store._add_chunks_to_collection(all_chunks, user_id)

        stats = vector_store.document_processor.get_chunk_info(all_chunks)
        return {"message": f"Traité {len(all_chunks)} chunks", "stats": stats}

    except Exception as e:
        logging.error(f"Erreur lors du traitement: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@app.post("/pdfs/process-by-file")
def process_pdfs_by_file(data: ProcessPdfByFileInput):
    """
    Traite les PDFs fichier par fichier avec limitation
    """
    try:
        user_id = data.user_id

        if not user_id:
            raise HTTPException(status_code=400, detail="user_id est requis")

        custom_pdf_path = data.custom_pdf_path

        pdf_path = Path(custom_pdf_path) if custom_pdf_path else PDF_PATH

        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="Dossier PDF non trouvé")

        list_pdf: List[Path] = get_pdf_files(PDF_PATH, EXTENSIONS)

        if not list_pdf:
            raise HTTPException(status_code=404, detail="Aucun fichier PDF trouvé")
        
        limited_files = list_pdf[:data.max_files]

        results = []
        total_chunks_added = 0

        for pdf_file in limited_files:
            try:
                # Traite un fichier à la fois
                chunks = vector_store.document_processor.process_file(pdf_file)

                if chunks:
                    # Ajoute à la collection
                    vector_store._add_chunks_to_collection(chunks, user_id)

                    results.append({
                        "file": pdf_file.name,
                        "chunks": len(chunks),
                        "status": "success"
                    })
                    total_chunks_added += len(chunks)
                else:
                    results.append({
                        "file": pdf_file.name,
                        "chunks": 0,
                        "status": "no_content"
                    })

            except Exception as e:
                logging.error(f"Erreur avec {pdf_file}: {e}")
                results.append({
                    "file": pdf_file.name,
                    "chunks": 0,
                    "status": f"error: {str(e)}"
                })

        return {
            "message": f"Traité {len(limited_files)} fichiers",
            "total_chunks": total_chunks_added,
            "results": results
        }

    except Exception as e:
        logging.error(f"Erreur lors du traitement par fichier: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@app.post("/upload-documents")
async def upload_documents(
    user_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Upload et traitement de documents"""
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id est requis")

        file_paths = []
        for file in files:
            temp_path = f"./temp/{file.filename}"
            os.makedirs("./temp", exist_ok=True)

            content = await file.read()
            
            with open(temp_path, "wb") as f:
                f.write(content)
            file_paths.append(temp_path)

        stats = vector_store.add_documents_from_files(file_paths, user_id)

        for path in file_paths:
            try:
                os.remove(path)
            except Exception as e:
                logging.warning(f"Impossible de supprimer {path}: {e}")

        return {"message": "Documents traités", "stats": stats}

    except Exception as e:
        logging.error(f"Erreur upload documents: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@app.get("/collection/size")
def get_collection_size(user_id: str):
    """Retourne la taille de la collection"""
    size = vector_store.get_collection_size(user_id)
    return {"collection_size": size}


@app.delete("/collection/clear")
def clear_collection(user_id: str):
    """Vide complètement la collection de l'utilisateur"""
    success = vector_store.clear_collection(user_id)
    if success:
        return {"message": "Collection vidée avec succès"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors du vidage")


@app.get("/files")
def get_files_list(user_id: str):
    """Liste tous les fichiers indexés de l'utilisateur"""
    files = vector_store.get_file_list(user_id)
    return {"files": files}


@app.delete("/files")
def delete_file(data: DeleteFileInput):
    """Supprime tous les chunks d'un fichier spécifique de l'utilisateur"""
    user_id = data.user_id
    file_name = data.file_name

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id est requis")

    success = vector_store.delete_file_chunks(file_name, user_id)
    
    if success:
        return {"message": f"Fichier {file_name} supprimé avec succès"}
    else:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de {file_name}")


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(
        level=logging.INFO,
        filename="main.log",
        filemode="w",
        encoding="utf-8"
    )

    # Crée les dossiers nécessaires
    PDF_PATH.mkdir(exist_ok=True)
    Path("./temp").mkdir(exist_ok=True)

    uvicorn.run(app, port=8000)