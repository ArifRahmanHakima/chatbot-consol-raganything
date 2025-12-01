# src/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.config.rag_config import get_rag


app = FastAPI()
rag = get_rag()

class QuestionRequest(BaseModel):
    question: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/ui"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("src/ui/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.on_event("startup")
async def init_lightrag():
    print("🔄 Initializing LightRAG from rag_storage...")
    await rag.process_document_complete(
        file_path="data/jdih.pdf",
        output_dir="rag_storage",
        parse_method="auto",
        display_stats=False
    )
    print("✅ LightRAG is now ready and loaded!")

@app.post("/ask")
async def ask_endpoint(req: QuestionRequest):
    answer = await rag.aquery(
        req.question,
        mode="local",
        vlm_enhanced=False,
        top_k=5
    )
    return {"answer": answer.strip()}
