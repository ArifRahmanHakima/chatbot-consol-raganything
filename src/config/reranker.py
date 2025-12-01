from sentence_transformers import CrossEncoder

ENABLE_RERANK = True
TOP_K = 5

# Tambahan penting
MAX_INPUT_TOKENS = 2048
MAX_OUTPUT_TOKENS = 1000

if ENABLE_RERANK:
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
else:
    reranker = None

def rerank_results(query, documents, top_k=TOP_K):
    print(f"🔁 RERANK ACTIVE — reranking {len(documents)} chunks")
    if not reranker or not documents:
        print("⚠️ Reranker tidak aktif atau dokumen kosong.")
        return documents[:top_k]

    print(f"🔁 Menjalankan reranker untuk query: {query}")
    scores = reranker.predict([[query, doc] for doc in documents])
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:top_k]]

