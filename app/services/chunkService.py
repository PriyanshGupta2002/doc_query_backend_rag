# from typing import List
# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# def create_document_chunks(
#     documents: List[Document],
#     chunk_size: int = 1000,
#     chunk_overlap: int = 200
# ) -> List[Document]:

#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         length_function=len,
#         separators=["\n\n", "\n", " ", ""]
#     )

#     return text_splitter.split_documents(documents)

from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def clean_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def create_document_chunks(
    documents: List[Document],
    chunk_size: int = 1800,
    chunk_overlap: int = 300
) -> List[Document]:

    # Clean documents
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    # Token-aware splitter
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    # Add chunk ids
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    return chunks