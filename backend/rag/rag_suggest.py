import os
import shutil
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI API KEY not found.")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")



class TensorFlowHuggingFaceEmbeddings(Embeddings):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = TFAutoModel.from_pretrained(model_name, from_pt=True)

    def _embed(self, texts: list[str]) -> list[list[float]]:
        inputs = self.tokenizer(
            texts, padding=True, truncation=True, return_tensors="tf"
        )
        outputs = self.model(**inputs)
        last_hidden_state = outputs.last_hidden_state
        attention_mask = tf.cast(inputs["attention_mask"], tf.float32)
        masked_hidden_state = last_hidden_state * tf.expand_dims(attention_mask, -1)
        summed_hidden_state = tf.reduce_sum(masked_hidden_state, axis=1)
        summed_mask = tf.reduce_sum(attention_mask, axis=1)
        pooled_embeddings = summed_hidden_state / tf.expand_dims(summed_mask, -1)
        normalized_embeddings = tf.math.l2_normalize(pooled_embeddings, axis=1)
        return normalized_embeddings.numpy().tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text])[0]



def generate_suggested_headers(input_text: str) -> str:

    persist_directory = "backend/vector_store_temp"

    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    os.makedirs(persist_directory, exist_ok=True)

    if not input_text or not input_text.strip():
        return "Input string is empty. Cannot generate headers."

    document = [Document(page_content=input_text)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(document)
    embedder = TensorFlowHuggingFaceEmbeddings()
    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embedder, persist_directory=persist_directory
    )

    retrieved_docs = vectordb.similarity_search("ESG report", k=5)
    context = "\n---\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""
    You are an expert technical writer specializing in creating well-structured Environmental, Social, and Governance (ESG) reports.
    Based on the provided context from a document, generate a list of 5-7 relevant headers. For each header, provide 2-3 logical subheaders.
    
    DOCUMENT TOPIC: "ESG report"

    RETRIEVED CONTEXT:
    ---
    {context}
    ---

    Format the output like this:
    1 Header
    1.1 Subheader
    1.2 Subheader
    2 Header
    2.1 Subheader
    2.2 Subheader
    """

    try:
        response = gemini_model.generate_content(prompt)
        shutil.rmtree(persist_directory)
        return response.text
    except Exception as e:
        shutil.rmtree(persist_directory)
        return f"An error occurred while generating content: {e}"



# Testing Block 
# if __name__ == "__main__":
#     print("Running ....")

#     # Sample text for testting
#     esg_document_content = """
#     Our company is committed to reducing its carbon footprint by 20% by 2030.
#     We have invested in renewable energy sources, including solar panel installations at our major facilities.
#     Water consumption has been decreased by 15% through recycling initiatives.
#     On the social front, we prioritize diversity and inclusion, with a 40% female representation in management roles.
#     Employee wellness programs have been expanded.
#     Our governance is overseen by an independent board with a dedicated ethics committee.
#     We maintain transparent reporting standards and comply with all regulatory frameworks.
#     """

#     suggested_structure = generate_suggested_headers(input_text=esg_document_content)

#     print("\nGenerated ESG Report Structure \n")
#     print(suggested_structure)
#     print(type(suggested_structure))
#     print("\nTest Finished \n\n")
