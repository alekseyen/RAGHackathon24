FROM langchain/langchain:0.1.0

# need only for pre processing stage
# RUN apt-get install -y tesseract-ocr-rus poppler-utils tesseract-ocr

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt


# Copy app code
COPY . .

# Run streamlit
# CMD ["streamlit", "run", "bot.py"]
EXPOSE 8501