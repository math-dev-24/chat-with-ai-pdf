import logging
from pathlib import Path

def save_resume(pdf_name: str, summary: str, resume_path: Path) -> str:
    resume_file = f"{pdf_name}.md"
    resume_path = resume_path / resume_file
    resume_path.write_text(summary, encoding='utf-8')

    logging.info(f"resume files write for : {pdf_name} at {resume_path}")

    return resume_file


def create_markdown(
        pdf_name: str,
        pdf_path: Path,
        text: str,
        images: list[str],
        resume_filename: str,
        note_path_const: Path,
        pdf_path_const: Path
):
    img_md = "\n".join(f"![[Images/{pdf_name}/{img}]]" for img in images)


    md_content = f"""# {pdf_name}

📎 Fichier original : 
- [[{pdf_path.name}]]

🧠 Résumé : 
- [[Resumes/{resume_filename}]]

---
## 🖼️ Images extraites
{img_md if images else "_Aucune image extraite._"}
"""
    md_file = note_path_const / f"{pdf_name}.md"
    md_file.write_text(md_content, encoding='utf-8')

    logging.info(f"markdown files created for : {pdf_name} at : {md_file}")