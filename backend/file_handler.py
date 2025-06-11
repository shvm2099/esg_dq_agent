import os
import tempfile
from typing import List

from fastapi import UploadFile 

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)

async def extract_text_from_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[-1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    if ext == ".pdf":
        loader = PyPDFLoader(temp_file_path)
    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(temp_file_path)
    elif ext == ".txt":
        loader = TextLoader(temp_file_path)
    else:
        os.remove(temp_file_path)
        raise ValueError(f"Unsupported file format: {ext}")

    try:
        docs: List[Document] = loader.load()
    finally:
        os.remove(temp_file_path)

    return "\n\n".join([doc.page_content for doc in docs])

