from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_voyageai import VoyageAIEmbeddings

load_dotenv()

urls = [
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

doc_splits = text_splitter.split_documents(docs_list)

# vectorstore = Chroma.from_documents(
#     documents=doc_splits,
#     collection_name="rag-chroma",
#     embedding=VoyageAIEmbeddings(
#         model="voyage-4-lite", show_progress_bar=True, batch_size=10
#     ),
#     persist_directory="./.chroma"
# )

retriever = Chroma(
    collection_name="rag-chroma",
    embedding_function=VoyageAIEmbeddings(
        model="voyage-4-lite", show_progress_bar=True, batch_size=10
    ),
    persist_directory="./.chroma"
).as_retriever()