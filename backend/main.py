from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routes import process
from backend.routes import metadata 

app = FastAPI()

app.include_router(process.router)
app.include_router(metadata.router)

app.mount("/pdfs", StaticFiles(directory="backend/generated_pdfs"), name="pdfs")
app.mount("/compliance_reports", StaticFiles(directory="backend/compliance_reports"), name="compliance_reports")
app.mount("/metadata", StaticFiles(directory="backend/metadata"), name="metadata")
