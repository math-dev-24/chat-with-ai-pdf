import logging, os
import time
# ______________________________________________________________________________________________________________________
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
# ______________________________________________________________________________________________________________________
from src.application.adapters.ai_chat.openAI import OpenAiConnector
from src.domain.services.ai_service import AiService
from src.api.schemas.chat_input import AskDataInput
from src.api.schemas.chat_response import AskDataResponse
from src.api.schemas.history import HistoryMessage
from src.domain.services.vector_service import VectorStore
from src.tools.file import get_pdf_files
# ______________________________________________________________________________________________________________________
load_dotenv()
# ______________________________________________________________________________________________________________________
PDF_PATH = Path(os.getenv("PDF_PATH"))
EXTENSIONS: list[str] = ["pdf"]
# ______________________________________________________________________________________________________________________
app = FastAPI()

html_path = Path("./src/front")
app.mount("/static", StaticFiles(directory=html_path, html=True), name="static")

ai_service = AiService(OpenAiConnector())
vector_store = VectorStore()

@app.get("/")
async def root():
    return RedirectResponse(url="/static/html/index.html")

@app.get("/documentation")
async def documentation():
    return RedirectResponse(url="/static/html/documentation.html")

@app.get("/pdfs")
async def pdfs():
    return RedirectResponse(url="/static/html/pdf.html")

@app.get("/stat")
def get_stat():
    return vector_store.get_collection_stats()

@app.post("/ask", response_model=AskDataResponse)
def ask(data: AskDataInput):
    try:
        start_time = time.time()

        context = vector_store.get_context_for_query(
            query=data.question,
            max_context_length=data.max_context_length
        )

        history_context = data.get_formatted_history()

        ai_response = ai_service.response(
            question=data.question,
            context=context,
            history=history_context
        )

        updated_history = data.historics.copy()
        updated_history.append(HistoryMessage(role="user", content=data.question))
        updated_history.append(HistoryMessage(role="assistant", content=ai_response))

        processing_time = time.time() - start_time

        return AskDataResponse(
            question=data.question,
            response=ai_response,
            context=context,
            context_length=len(context),
            sources_count=context.count("---") + 1,
            processing_time=processing_time,
            updated_history=updated_history
        )

    except Exception as e:
        logging.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pdfs/process-all")
def process_all_pdfs():
    """Traite tous les PDFs du dossier configuré avec limitation"""
    chunk_limit = 1000

    try:
        if not PDF_PATH.exists():
            raise HTTPException(status_code=404, detail="Dossier PDF non trouvé")

        list_pdf: List[Path] = get_pdf_files(PDF_PATH, EXTENSIONS)

        # Traitement avec limitation de chunks
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
            vector_store._add_chunks_to_collection(all_chunks)

        stats = vector_store.document_processor.get_chunk_info(all_chunks)
        return {"message": f"Traité {len(all_chunks)} chunks", "stats": stats}

    except Exception as e:
        logging.error(f"Erreur lors du traitement: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@app.post("/pdfs/process-by-file")
def process_pdfs_by_file(max_files: int = 5):
    """
    Traite les PDFs fichier par fichier avec limitation
    """
    try:
        if not PDF_PATH.exists():
            raise HTTPException(status_code=404, detail="Dossier PDF non trouvé")

        list_pdf: List[Path] = get_pdf_files(PDF_PATH, EXTENSIONS)

        # Limite le nombre de fichiers
        limited_files = list_pdf[:max_files]

        results = []
        total_chunks_added = 0

        for pdf_file in limited_files:
            try:
                # Traite un fichier à la fois
                chunks = vector_store.document_processor.process_file(pdf_file)

                if chunks:
                    # Ajoute à la collection
                    vector_store._add_chunks_to_collection(chunks)

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
async def upload_documents(files: List[UploadFile]):
    """Upload et traitement de documents"""
    try:
        file_paths = []
        for file in files:
            temp_path = f"./temp/{file.filename}"
            # Crée le dossier temp s'il n'existe pas
            os.makedirs("./temp", exist_ok=True)

            with open(temp_path, "wb") as f:
                f.write(await file.read())
            file_paths.append(temp_path)

        # Utilise la méthode principale pour traiter les fichiers
        stats = vector_store.add_documents_from_files(file_paths)

        # Nettoyage des fichiers temporaires
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
def get_collection_size():
    """Retourne la taille de la collection"""
    size = vector_store.get_collection_size()
    return {"collection_size": size}


@app.delete("/collection/clear")
def clear_collection():
    """Vide complètement la collection"""
    success = vector_store.clear_collection()
    if success:
        return {"message": "Collection vidée avec succès"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors du vidage")


@app.get("/files")
def get_files_list():
    """Liste tous les fichiers indexés"""
    files = vector_store.get_file_list()
    return {"files": files}


@app.delete("/files/{file_name}")
def delete_file(file_name: str):
    """Supprime tous les chunks d'un fichier spécifique"""
    success = vector_store.delete_file_chunks(file_name)
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