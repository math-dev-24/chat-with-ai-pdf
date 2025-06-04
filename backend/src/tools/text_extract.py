from typing import List, Dict
import re, fitz


class PDFChapterExtractor:
    def __init__(self, pdf_path: str):
        self.doc = fitz.open(pdf_path)

        # Correction des regex (remplace /s par \s et /d par \d)
        self.chapter_patterns = [
            # Avec numéros romains: I. GENERALITE, II. CONCEPTION
            r'^[IVX]+\.\s+[A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ][A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ\s]+$',
            # Avec numéros: 1. Rôles, 2. Reserve de liquide
            r'^\d+\.\s+[A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ][^.]*$',
            # Titres en majuscules: TECHNOLOGIE DU FROID, SOMMAIRE
            r'^[A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ][A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ\s:]{10,}$',
            # Sections numérotées: 3.1.Les séparateurs horizontaux
            r'^\d+\.\d+\.[A-ZÀ-Ÿ][^.]*$',
            # Titres avec tirets ou underscores
            r'^[A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ][A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ\s\-_:]{8,}$',
            # Détection générale: ligne courte, principalement en majuscules
            r'^[A-ZÀÉÈÊËÏÎÔÖÙÛÜŸÇ][A-Za-zÀ-ÿ\s\-:]{5,50}$'
        ]

    def extract_chapters(self) -> List[Dict[str, str]]:
        """
        Extrait le contenu par chapitres
        Returns: Liste de dict avec {'title': str, 'content': str}
        """
        chapters = []
        current_title = None
        current_content = []

        for page_num, page in enumerate(self.doc, 1):
            text = page.get_text("text")

            lines = text.split('\n')

            cleaned_lines = self._clean_lines(lines)

            for line in cleaned_lines:
                line = line.strip()
                if not line:
                    continue

                if self._is_chapter_title(line):
                    if current_title and current_content:
                        chapters.append({
                            'title': current_title,
                            'content': '\n'.join(current_content).strip()
                        })

                    current_title = line
                    current_content = []
                else:
                    if current_title:
                        current_content.append(line)

        if current_title and current_content:
            chapters.append({
                'title': current_title,
                'content': '\n'.join(current_content).strip()
            })

        if not chapters:
            all_text = self._extract_all_text()
            chapters.append({
                'title': 'Document complet',
                'content': all_text
            })

        return chapters

    def _clean_lines(self, lines: List[str]) -> List[str]:
        """Supprime les headers/footers répétitifs"""
        cleaned = []

        for line in lines:
            line = line.strip()

            # Ignorer les éléments répétitifs (corrections des regex)
            skip_patterns = [
                r'^BERTRAND\s*-\s*BOUTEILLE\s*-\s*DESNOS',
                r'^TECHNOLOGIE DU FROID\s*:\s*ASPECT',
                r'^Fiche technique',
                r'^\d+$',
                r'^Page\s+\d+',
                r'^\s*$'
            ]

            if any(re.match(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
                continue

            cleaned.append(line)

        return cleaned

    def _is_chapter_title(self, line: str) -> bool:
        """Détermine si une ligne est un titre de chapitre"""
        # Ignorer les lignes trop longues (probablement du contenu)
        if len(line) > 80:
            return False

        # Ignorer les lignes qui commencent par des minuscules ou des symboles
        if line and line[0].islower():
            return False

        # Ignorer les lignes qui ressemblent à des formules ou du contenu
        if any(char in line for char in ['=', '+', '-', '×', '÷', '(', ')', '[', ']']):
            return False

        # Vérifier contre les patterns
        for pattern in self.chapter_patterns:
            if re.match(pattern, line):
                return True

        # Heuristique supplémentaire: ligne courte avec beaucoup de majuscules
        if len(line) <= 60 and sum(1 for c in line if c.isupper()) >= len(line) * 0.6:
            # Mais pas si c'est juste des chiffres et ponctuation
            if re.search(r'[A-ZÀ-Ÿ]{3,}', line):
                return True

        return False

    def _extract_all_text(self) -> str:
        """Extrait tout le texte comme fallback"""
        all_text = []
        for page in self.doc:
            text = page.get_text("text")
            lines = self._clean_lines(text.split('\n'))  # Correction: \n
            all_text.extend(lines)

        return '\n'.join(all_text)  # Correction: \n

    def close(self):
        """Ferme le document PDF"""
        self.doc.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()