
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
os.environ["USE_TF"] = "1"
os.environ["USE_TORCH"] = "0"


def ingest_reference_docs(reference_folder="backend/reference_docs"):
    loader = TextLoader(os.path.join(reference_folder, "sample_ref.txt")) 
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=25)
    chunks = splitter.split_documents(documents)

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embedding=embedder, persist_directory="backend/vector_store")
    vectordb.persist()


