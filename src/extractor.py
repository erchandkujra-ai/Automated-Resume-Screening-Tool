
from pathlib import Path
import pdfplumber
from docx import Document


def extract_text(file_path):
    """
    Extract text from PDF, DOCX, or TXT resume.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        text = ""

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text.strip()

    elif extension == ".docx":
        document = Document(path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        return "\n".join(paragraphs).strip()

    elif extension == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    else:
        raise ValueError(
            "Unsupported file format. Use PDF, DOCX, or TXT."
        )
