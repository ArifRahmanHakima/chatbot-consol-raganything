from lightrag.utils import EmbeddingFunc
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid
import time

# Inisialisasi model embedding
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Client baru (sesuai dokumentasi)
client = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection(name="document_embeddings")

# Embedding tanpa chunking
async def local_embedding(texts):
    start = time.time()

    if isinstance(texts, str):
        texts = [texts]

    # Langsung embedding seluruh teks tanpa chunking
    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=16,  
        show_progress_bar=True
    )

    # Simpan embeddings ke ChromaDB
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": "document"}] * len(texts),
        ids=[str(uuid.uuid4()) for _ in range(len(texts))]
    )

    print(f"✅ Embed selesai dalam {time.time() - start:.2f} detik")
    return embeddings

embedding_func = EmbeddingFunc(
    embedding_dim=384,
    max_token_size=512,
    func=local_embedding,
)
