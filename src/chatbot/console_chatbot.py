import asyncio
import sys
from src.config.rag_config import get_rag
from datetime import datetime
from src.config.reranker import rerank_results
from lightrag.base import QueryParam


# Warna (ANSI escape codes — opsional)
class Style:
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"


def log_info(msg: str):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"{Style.BLUE}[{now}] {msg}{Style.RESET}")


def print_header():
    print("\n" + "=" * 60)
    print(f"{Style.BOLD}🤖 Selamat datang di RAGAnything Chatbot!{Style.RESET}")
    print("Ketik pertanyaan kamu di bawah ini.")
    print("Ketik 'exit' untuk keluar kapan saja.")
    print("=" * 60)


async def main():
    rag = get_rag()

    try:
        log_info("📦 Memuat data dari rag_storage...")
        await rag.process_document_complete(
            file_path="data/jdih.pdf",
            output_dir="rag_storage",
            parse_method="auto",
            display_stats=False
        )
        log_info(f"{Style.GREEN}✅ Data berhasil dimuat dari cache atau sudah diproses sebelumnya!{Style.RESET}\n")

    except Exception as e:
        print(f"{Style.RED}❌ Gagal memuat dokumen: {e}{Style.RESET}")
        print("🔁 Pastikan file PDF tersedia dan sudah bisa diproses.")
        sys.exit(1)

    print_header()

    while True:
        try:
            question = input(f"\n{Style.YELLOW}📝 Pertanyaan: {Style.RESET}").strip()

            if question.lower() in ['exit', 'quit', 'keluar']:
                print(f"{Style.GREEN}👋 Terima kasih! Sampai jumpa!{Style.RESET}\n")
                break

            if not question:
                continue

            print(f"{Style.BLUE}🔎 Sedang mencari jawaban...\n{Style.RESET}")
            result = await rag.aquery(
                question,
                mode="local",
                vlm_enhanced=False,
                top_k=5
            )

            print(f"{Style.GREEN}💡 Jawaban:\n{Style.RESET}{result.strip()}\n")
            print("-" * 60)

        except KeyboardInterrupt:
            print(f"\n\n{Style.RED}👋 Chatbot dihentikan oleh user.{Style.RESET}")
            break
        except Exception as e:
            print(f"{Style.RED}❌ ERROR: {e}{Style.RESET}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Style.RED}👋 Exit by user.{Style.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Style.RED}❌ Fatal Error: {e}{Style.RESET}")
        sys.exit(1)