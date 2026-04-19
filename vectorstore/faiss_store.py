from langchain_community.vectorstores import FAISS

_vector_store_cache = {}

def get_or_create_vector_store(text: str, chunks: list, embeddings):
    text_hash = hash(text)
    if text_hash in _vector_store_cache:
        return _vector_store_cache[text_hash]
    
    vector_store = FAISS.from_texts(chunks, embeddings)
    _vector_store_cache[text_hash] = vector_store
    return vector_store
