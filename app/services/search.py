from app.services.retreival import retrieve_documents
from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY
from app.utils.responseCleaner import clean_llm_response
# 🔥 create once (not inside function)
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0.1,
    max_tokens=1024,
)

def search(doc_id: int, query: str):
    results = retrieve_documents(query=query, doc_id=doc_id)

    if not results:
        return "No relevant information found in the document."

    context = "\n\n".join([
        f"Document {i}:\n{doc['content']}"
        for i, doc in enumerate(results)
    ])

    prompt = f"""
You are a helpful assistant.

STRICT RULES:
- Answer ONLY using the provided context
- Do NOT include references like "Document", "L1-L4", "†", or any symbols
- Do NOT write escape sequences — never write \\n, write an actual line break instead
- Use bullet points only if necessary
- Keep formatting clean and readable

Context:
{context}

Question: {query}

Answer:
"""

    response = llm.invoke(prompt)
    cleaned = clean_llm_response(response.content)
    return cleaned