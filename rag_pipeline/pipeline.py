from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings.google_embeddings import get_google_embeddings
from vectorstore.faiss_store import get_or_create_vector_store

def get_relevant_context(text: str, query: str, k: int = 3) -> str:
    """
    Takes full transcript and query,
    returns top relevant chunks combined as context.
    """
    if not text.strip():
        return ""

    # 1. Chunk text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    
    if not chunks:
        return ""
        
    # 2. Get embeddings module
    embeddings = get_google_embeddings()
    
    # 3. Store or retrieve from FAISS vectorstore
    vector_store = get_or_create_vector_store(text, chunks, embeddings)

    # 4. Embed query & 5. Retrieve top-k chunks
    docs = vector_store.similarity_search(query, k=k)
    
    # 6. Return combined context
    context = "\n...\n".join([doc.page_content for doc in docs])
    return context
