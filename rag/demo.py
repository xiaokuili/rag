#  demo

# load->split->embeding->retriever->llm
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

from typing import Any, Dict, Iterator, List, Optional, Sequence, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_core.vectorstores import VectorStore
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.csv_loader import CSVLoader



import os
# config
load_dotenv()  # take environment variables from .env.
# sqlite3 
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# qianfan
os.environ["QIANFAN_AK"] = os.getenv("QIANFAN_AK")
os.environ["QIANFAN_SK"] = os.getenv("QIANFAN_SK")
# split 
chunk_size=100
chunk_overlap=20


def load(path: str)-> List[Document]:
    # Only keep post title, headers, and content from the full HTML.
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    return Document(page_content=html, metadata={"source": path})


def split(docs: Sequence[Document]) ->  List[Document]:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits

def embeding_store(docs: Sequence[str], query: str=None) -> VectorStore :
    if not docs:
        raise ValueError("No documents to embed.")
    
    embed = QianfanEmbeddingsEndpoint()
    db = Chroma.from_documents(docs, embed)
    # query it
    if query:
        docs = db.similarity_search(query)
        print("rst", docs[0].page_content)

    return db

def retriever(vectorstore: VectorStore, query: str) ->  Document:
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    retrieved_docs = retriever.invoke(query)
    return retrieved_docs

def generator( url: str, query: str) ->  Document:    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    docs = split(load(url))
    vectorstore = embeding_store(docs)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    rst = rag_chain.invoke(query)
    print(rst)




# test
url = "http://www.news.cn/fortune/2023-08/21/c_1129813265.htm"

def load_test():
    load(url)

def split_test():
    docs = load(url)
    print(docs)
    split(docs)


def embeding_store_test():
    query = "什么是老三样"
    docs = split(load(url))
    embeding_store(docs, query)


def retriever_test():
    query = "什么是老三样"
    docs = split(load(url))
    for item in docs:
        print(item)
        print("\n")
    db = embeding_store(docs, "")
    rst_docs = retriever(db, query)
    for doc in rst_docs:
        print(doc)
        print("\n")


def generator_test():
    query = "什么是老三样"
    generator( url, query)

if __name__ == '__main__':
    generator_test()