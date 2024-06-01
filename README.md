# Command to start

sudo apt-get install tesseract-ocr-rus poppler-utils tesseract-ocr

1. DO the OCR [via Yandex API or XXX]

   1.1 Yandex OCR

   ```
   DOCX_DIR=dock_folder python3 __main__.py --pdf_path "raw_pdf/машинписное/Summary_MICEX-RTS_FS_4Q2022_RUS.pdf" --language_code ru,en
   ```

   1.2. unstructured.partition.pdf

   File `ocr_pre_process.py`
   

2. Create FAISS DB:
   cd "rag/tools/2. create_rag_db"
   python **main**.py --load_data_patch "rag/raw_pdf"
3. Search in FAISS DB: via laching bot.py

# Install env

```bash
conda create --name rag_hackathon python=3.10
conda activate rag_hackathon
pip install -r requirements.txt
```
