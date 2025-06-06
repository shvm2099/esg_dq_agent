import fitz
from docx import Document
import io

async def extract_text_from_file(file):
    if file.filename.endswith(".pdf"):
        pdf_bytes = await file.read()
        doc= fitz.open (stream= pdf_bytes, filetype = "pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    elif file.filename.endswith(".docx"):
        docx_bytes = await file.read()
        doc = Document(io.BytesIO(docx_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return (await file.read()).decode("utf-8")
    