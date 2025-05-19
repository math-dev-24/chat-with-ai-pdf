import os
import re
import fitz
import logging
# ______________________________________________________________________________________________________________________
from pathlib import Path
from dotenv import load_dotenv
# ______________________________________________________________________________________________________________________
from adapters.ai.openAi import OpenAiConnector
from domain.services.AiService import AiService
from tools.file import get_pdf_files
from tools.obsidian import save_resume, create_markdown
from tools.pdf import extract_text, extract_images
# ______________________________________________________________________________________________________________________
load_dotenv()
# ______________________________________________________________________________________________________________________
# Const
PDF_PATH = Path(os.getenv("PDF_PATH"))
IMG_PATH = Path(os.getenv("IMG_PATH"))
RESUME_PATH = Path(os.getenv("RESUME_PATH"))
NOTE_PATH = Path(os.getenv("NOTE_PATH"))

EXTENSIONS: list[str] = ["pdf"]
# ______________________________________________________________________________________________________________________

def process_pdf(pdf_path: Path) -> None:
    """
    :param pdf_path: path of pdf file
    :return: none
    """
    pdf_name: str = re.sub(" ", "_", pdf_path.stem)

    print(f"🔍 Treatment : {pdf_name}")

    doc = fitz.open(pdf_path)

    text = extract_text(doc)

    path_img = Path(os.path.join(IMG_PATH, pdf_name))

    if not os.path.exists(path_img):
        os.mkdir(path_img)

    images: list[str] = extract_images(doc, pdf_name, path_img)

    connector = OpenAiConnector()
    service = AiService(connector)

    summary = service.summarize(pdf_name, text)

    resume_filename = save_resume(pdf_name, summary, RESUME_PATH)

    create_markdown(pdf_name, pdf_path, text, images, resume_filename, NOTE_PATH, PDF_PATH)


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        filename="main.log",
        filemode="w",
        encoding="utf-8"
    )

    # search files sources
    files = get_pdf_files(PDF_PATH, extensions=EXTENSIONS)

    print(f"📂 Found {len(files)} PDF(s)")
    logging.info(f"📂 Found {len(files)} PDF(s)")

    for index, file in enumerate(files):
        print(f"🤖 {index + 1} / {len(files)}")

        try:
            process_pdf(file)
        except Exception as e:
            logging.error(f"❌ Error ({file.name}): {e}")
            print(f"❌ Erreur avec {file.name} : {e}")
