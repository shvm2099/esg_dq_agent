import os
from datetime import datetime
import pdfkit
from markdown2 import markdown

def generate_pdf(text: str, folder="backend/generated_pdfs") -> str:
    os.makedirs(folder, exist_ok=True)

    html = markdown(text)

    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    filename = f"processed_{timestamp}.pdf"
    pdf_path = os.path.join(folder, filename)

    pdfkit.from_string(html, pdf_path)

    return filename
