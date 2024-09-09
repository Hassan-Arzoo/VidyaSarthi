from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
import os


files = ["AUBrochure", "AUBrochureinternational"]
documents = []

for i in files:
    filepath = './KnowledgeBase/'+f'{i}.pdf'
    loader = PyPDFLoader(file_path=filepath)
    pages = loader.load_and_split()
    documents.extend(pages)

# filename = "rules_2014"
# filepath = './KnowledgeBase/'+f'{filename}.pdf'

# loader = PyPDFLoader(file_path=filepath)

# pages = loader.load_and_split()

# deployment_name = os.environ['OPENAI_EMBEDDING_MODEL_NAME']
# model_name = os.environ['OPENAI_EMBEDDING_DEPLOYMENT_NAME']
# deployment_endpoint = os.environ['OPENAI_EMBEDDING_DEPLOYMENT_ENDPOINT']
# deployment_version = os.environ['OPENAI_EMBEDDING_DEPLOYMENT_VERSION']
# api_key = os.environ['OPENAI_EMBEDDING_API_KEY']
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# embeddings = OpenAIEmbeddings(model=model_name,
#                               deployment=deployment_name,
#                               openai_api_base=deployment_endpoint,
#                               openai_api_key=api_key,
#                               openai_api_type='azure',
#                               openai_api_version=deployment_version)
embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)

fs = LocalFileStore("./indexes/cache/")

cache_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=embeddings,
    document_embedding_cache=fs,
    namespace=embeddings.model
)


# db = FAISS.from_documents(documents=pages, embedding=cache_embedder)
db = FAISS.from_documents(documents=documents, embedding=cache_embedder)

db.save_local(f"./indexes/combined-docs")

print("Embeddings created successfully.")
