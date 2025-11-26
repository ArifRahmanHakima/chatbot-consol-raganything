# 🤖 RAG-Anything Chatbot consol simple

Chatbot terminal berbasis dokumen PDF yang dibangun menggunakan [RAG-Anything](https://github.com/HKUDS/RAG-Anything), mendukung pencarian informasi multimodal (teks, gambar, tabel, rumus) secara efisien. Proyek ini dikembangkan sebagai bagian dari kegiatan magang.

---

## 📌 Fitur Utama

* 🔍 **Pencarian berbasis RAG (Retrieval-Augmented Generation)**
* 📄 **Parsing dokumen otomatis** menggunakan MinerU
* 💬 **Chatbot terminal interaktif** dengan dukungan histori pertanyaan
* 🧠 **Model embedding lokal** (`all-MiniLM-L6-v2`)
* 🌐 **LLM via OpenRouter API** (`gpt-4o`, `gpt-4o-mini`)

---

## 🗂️ Struktur Proyek

```
rag-anything-chatbot/
├── data/                  # Folder PDF input
│   ├── you_scan.pdf
│   ├── you_teks.pdf
│   └── ...
├── rag_storage/           # Output hasil parsing dan embedding
├── .env                   # File API dan nama model
├── requirements.txt       # Dependensi proyek
├── rag_config.py          # Konfigurasi model dan pipeline RAG
├── ingest_pipeline.py     # Script 1x: parsing + embedding dokumen
├── console_chatbot.py     # Chatbot interaktif berbasis terminal
└── README.md              # Dokumentasi proyek
```

---

## ⚙️ Instalasi

### 1. Clone Repositori

```bash
git clone https://github.com/namamu/rag-anything-chatbot.git
cd rag-anything-chatbot
```

### 2. Buat Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

---

## 🔐 Konfigurasi `.env`

Buat file `.env` di root folder, isi dengan:

```
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL= Masukan nama model dari openrouter
VISION_MODEL= Masukan nama model dari openrouter
```
---

## 🏁 Menjalankan Proyek

### 1. Letakkan dokumen ke folder `data/`

Contoh:

```
data/you_teks.pdf
```

### 2. Jalankan Ingest Pipeline (1x saja per dokumen)

```bash
python ingest_pipeline.py
```

### 3. Jalankan Chatbot Terminal

```bash
python console_chatbot.py
```

Contoh interaksi:

```
📝 Pertanyaan: Apa itu klasterisasi?
💡 Jawaban:
Klasterisasi adalah metode pengelompokan data berdasarkan kesamaan ...

📝 Pertanyaan: Jelaskan lebih lanjut
💡 Jawaban:
Metode seperti K-Means dan Agglomerative digunakan untuk ...
```

---


## 📌 Catatan Tambahan

* Folder `rag_storage/` menyimpan hasil parsing dan embedding.
* Jika ingin reset ulang, hapus `rag_storage/` dan jalankan ulang `ingest_pipeline.py`
* Semua query dijalankan secara asinkron (non-blocking, cepat)
* Bisa dikembangkan lebih lanjut ke Web UI berbasis FastAPI / HTMX / Vue / dll.

---

