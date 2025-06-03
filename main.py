import logging, os
import time
# ______________________________________________________________________________________________________________________
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
# ______________________________________________________________________________________________________________________
from src.application.adapters.ai_chat.openAI import OpenAiConnector
from src.domain.services.ai_service import AiService
from src.api.schemas.chat_input import AskDataInput
from src.api.schemas.chat_response import AskDataResponse
from src.api.schemas.history import HistoryMessage
from src.tools.file import get_pdf_files
# ______________________________________________________________________________________________________________________
from src.tools.init_vector_service import initialize_vector_service
# ______________________________________________________________________________________________________________________
load_dotenv()
# ______________________________________________________________________________________________________________________
PDF_PATH = Path(os.getenv("PDF_PATH"))
EXTENSIONS: list[str] = ["pdf"]
# ______________________________________________________________________________________________________________________
app = FastAPI()

html_path = Path("src/front/html")
app.mount("/static", StaticFiles(directory=html_path, html=True), name="static")

vector_service = initialize_vector_service()
ai_service = AiService(OpenAiConnector())

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/documentation")
async def documentation():
    return RedirectResponse(url="/static/documentation.html")

@app.get("/stat")
def get_stat():
    return vector_service.get_statistics()

@app.post("/ask", response_model=AskDataResponse)
def ask(data: AskDataInput):
    try:
        start_time = time.time()

        context = vector_service.get_context_for_query(
            query=data.question,
            max_context_length=data.max_context_length,
            prefer_chapters=data.prefer_chapters
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

@app.delete("/pdfs/{pdf_name}")
def remove_pdf(pdf_name: str):
    """Supprime un PDF de la base vectorielle"""
    try:
        pdf_path = PDF_PATH / pdf_name

        vector_service.remove_pdf_document(pdf_name, pdf_path)

        return {"success": True, "message": f"PDF {pdf_name} supprimé de la base vectorielle"}

    except Exception as e:
        logging.error(f"Erreur lors de la suppression du PDF {pdf_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")

@app.get("/pdfs/{pdf_name}/chapters")
def get_pdf_chapters(pdf_name: str):
    """Récupère la liste des chapitres d'un PDF"""
    try:
        filters = {"source_pdf": pdf_name, "content_type": "chapter"}
        search_results = vector_service.search_documents("", top_k=1000, filters=filters)

        chapters = []
        for result in search_results:
            metadata = result.document.metadata
            chapters.append({
                "index": metadata.get("chapter_index", 0),
                "title": metadata.get("chapter_title", "Sans titre"),
                "length": metadata.get("content_length", 0)
            })

        # Trier par index
        chapters.sort(key=lambda x: x["index"])

        return {
            "pdf_name": pdf_name,
            "chapters_count": len(chapters),
            "chapters": chapters
        }

    except Exception as e:
        logging.error(f"Erreur lors de la récupération des chapitres de {pdf_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/pdfs/process-all")
def process_all_pdfs():
    """Traite tous les PDFs du dossier configuré"""
    try:
        if not PDF_PATH.exists():
            raise HTTPException(status_code=404, detail="Dossier PDF non trouvé")

        processed = []
        errors = []

        for pdf_file in get_pdf_files(PDF_PATH, EXTENSIONS):
            try:
                vector_service.add_pdf_document_by_chapters(pdf_file)
                processed.append(pdf_file.name)
                logging.info(f"PDF traité: {pdf_file.name}")
            except Exception as e:
                errors.append({"file": pdf_file.name, "error": str(e)})
                logging.error(f"Erreur avec {pdf_file.name}: {e}")

        return {
            "success": True,
            "processed_count": len(processed),
            "processed_files": processed,
            "errors_count": len(errors),
            "errors": errors
        }

    except Exception as e:
        logging.error(f"Erreur lors du traitement batch: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(
        level=logging.INFO,
        filename="main.log",
        filemode="w",
        encoding="utf-8"
    )

    PDF_PATH.mkdir(exist_ok=True)

    uvicorn.run(app, port=8000)
