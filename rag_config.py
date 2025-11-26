import os
from dotenv import load_dotenv
from raganything import RAGAnything, RAGAnythingConfig
from lightrag.utils import EmbeddingFunc
from lightrag.llm.openai import openai_complete_if_cache
from sentence_transformers import SentenceTransformer

load_dotenv()

# Ambil API key dan base URL dari OpenRouter
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL")

# Ambil model LLM dari .env
LLM_MODEL = os.getenv("LLM_MODEL")
VISION_MODEL = os.getenv("VISION_MODEL")

# Gunakan model embedding lokal
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Fungsi untuk model teks (LLM)
def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
    return openai_complete_if_cache(
        LLM_MODEL,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=API_KEY,
        base_url=BASE_URL,
        max_tokens=1000,  # batasi token agar tidak error 402
        temperature=0.3,
        **kwargs,
    )


# Fungsi untuk model multimodal (image, table, etc.)
def vision_model_func(prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs):
    try:
        if messages:
            return openai_complete_if_cache(
                VISION_MODEL, "", system_prompt=None, history_messages=[],
                messages=messages, api_key=API_KEY, base_url=BASE_URL, **kwargs
            )
        elif image_data:
            return openai_complete_if_cache(
                VISION_MODEL, "", system_prompt=None, history_messages=[],
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]}
                ],
                api_key=API_KEY, base_url=BASE_URL, **kwargs
            )
        else:
            return llm_model_func(prompt, system_prompt, history_messages, **kwargs)
    except Exception as e:
        print(f"[Vision Model Fallback] Gagal memproses vision model ({VISION_MODEL}), pakai LLM biasa. Error: {e}")
        return llm_model_func(prompt, system_prompt, history_messages, **kwargs)


# Fungsi untuk model embedding lokal
async def local_embedding(texts):
    if isinstance(texts, str):
        texts = [texts]
    embeddings = embedding_model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


embedding_func = EmbeddingFunc(
    embedding_dim=384,
    max_token_size=512,
    func=local_embedding,
)


# Inisialisasi RAGAnything
def get_rag():
    config = RAGAnythingConfig(
        working_dir="./rag_storage",
        parser=os.getenv("PARSER", "mineru"),
        parse_method=os.getenv("PARSE_METHOD", "auto"),
        enable_image_processing=True,
        enable_table_processing=True,
        enable_equation_processing=True,
    )

    return RAGAnything(
        config=config,
        llm_model_func=llm_model_func,
        vision_model_func=vision_model_func,
        embedding_func=embedding_func,
    )
