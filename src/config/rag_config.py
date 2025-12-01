import os
from dotenv import load_dotenv
from raganything import RAGAnything, RAGAnythingConfig
from src.config.llm_router import llm_model_func
from src.config.embedder import embedding_func
from src.config.reranker import rerank_results  # 

load_dotenv()

def get_rag():
    config = RAGAnythingConfig(
        working_dir="./rag_storage",
        parser=os.getenv("PARSER", "mineru"),
        parse_method=os.getenv("PARSE_METHOD", "auto"),
        enable_image_processing=False,
        enable_table_processing=False,
        enable_equation_processing=False,
    )

    # Return RAGAnything instance without rerank_func directly in the constructor
    rag_instance = RAGAnything(
        config=config,
        llm_model_func=llm_model_func,
        embedding_func=embedding_func,
    )
    rag_instance.rerank_func = rerank_results
    return rag_instance
