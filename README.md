# Command to start

1. DO the OCR [via Yandex API or XXX]

    cd rag/tools/pdf_to_word_format

   ```
   DOCX_DIR=dock_folder python3 __main__.py --pdf_path "raw_pdf/машинписное/Summary_MICEX-RTS_FS_4Q2022_RUS.pdf" --language_code ru,en
   ```

2. Create FAISS DB:
    cd "rag/tools/2. create_rag_db"
    python __main__.py --load_data_patch "rag/raw_pdf"
    
3. Search in FAISS DB: via laching bot.py
    

# Install env

```bash
conda create --name rag_hackathon python=3.10
conda activate rag_hackathon
pip install -r requirements.txt
```
