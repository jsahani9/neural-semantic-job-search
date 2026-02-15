import fitz
from typing import BinaryIO


def extract_text_from_pdf(pdf_file: BinaryIO) -> str:
    try:
        pdf_bytes = pdf_file.read()

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        parts = []
        for page in doc:
            parts.append(page.get_text("text"))

        doc.close()

        text = "\n\n".join(parts).strip()

        if not text:
            raise ValueError("No text found in PDF")

        return text

    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")
