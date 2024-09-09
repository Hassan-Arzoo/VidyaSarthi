from langchain.chat_models import ChatOpenAI
import os
from langchain import FAISS, PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# OPENAI_DEPLOYMENT_ENDPOINT = os.environ["OPENAI_API_BASE"]
# OPENAI_DEPLOYMENT_NAME = os.environ["OPENAI_DEPLOYMENT_NAME"]
# OPENAI_MODEL_NAME = os.environ["OPENAI_MODEL_NAME"]
# OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.environ["OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
# OPENAI_EMBEDDING_MODEL_NAME = os.environ["OPENAI_EMBEDDING_MODEL_NAME"]
# OPENAI_DEPLOYMENT_VERSION = os.environ["OPENAI_API_VERSION"]


# Models
# llm = AzureChatOpenAI(deployment_name=OPENAI_DEPLOYMENT_NAME,
#                       model_name=OPENAI_MODEL_NAME,
#                       openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT,
#                       openai_api_version=OPENAI_DEPLOYMENT_VERSION,
#                       openai_api_key=OPENAI_API_KEY, verbose=True, request_timeout=30)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                 model="gpt-3.5-turbo",
                 streaming=True)

embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)
# # Embeddings
# embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL_NAME, chunk_size=1, deployment=OPENAI_EMBEDDING_DEPLOYMENT_NAME,
#                               openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT, openai_api_type='azure', openai_api_version=OPENAI_DEPLOYMENT_VERSION, request_timeout=30)

RETRIEVER_PROMPT_TEMPLATE = '''
You are VidyaSarthi, an AI-powered chatbot developed for the Department of Technical Education, Government of Rajasthan. 
Your role is to provide answers to queries related to various engineering and polytechnic institutes under your jurisdiction. 
You can provide information on admissions, eligibility, fees, scholarships, curriculum, placements, and more. 
Always answer from the context provided. If anyone asks a question outside of your knowledge base, deny politely to answer.
Do not make up any answers of your own.

Here is the context: {context}

Input Question: {question}

Answer:
'''


RETRIEVER_PROMPT = PromptTemplate(template=RETRIEVER_PROMPT_TEMPLATE, input_variables=[
                                  "context", "question"])


combined_rules_retriever = FAISS.load_local(
    "./indexes/combined-docs", embeddings, "index").as_retriever()

combined_rules_chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=combined_rules_retriever, chain_type_kwargs={"prompt": RETRIEVER_PROMPT, "verbose": True}, input_key="input", verbose=True)


def get_response(query):
    return combined_rules_chain.run(query)


# while (True):
#     userInput = input("Enter your Question/Queries (or 'exit' to quit): ")
#     if userInput == 'exit':
#         print('Thank you for contacting KhanijMitra. Apka din shubh ho!')
#         break
#     else:
#         print(combined_rules_chain.run(userInput))
