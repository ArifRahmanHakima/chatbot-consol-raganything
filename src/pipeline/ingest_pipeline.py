import asyncio
import sys
from src.config.rag_config import get_rag

async def main():
    rag = get_rag()

    try:
        print("📄 Memproses dokumen: data/jdih.pdf")
        
        # Proses dokumen
        await rag.process_document_complete(
            file_path="data/jdih.pdf",
            output_dir="rag_storage"
        )
        
        print("✅ Dokumen berhasil diproses!\n")
    except Exception as e:
        print(f"❌ ERROR saat parsing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
