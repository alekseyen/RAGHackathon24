FROM continuumio/anaconda3

# Create and activate environment
RUN conda create -y --name rag_hackathon
RUN conda activate rag_hackathon

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Run streamlit
CMD ["streamlit", "run", "bot.py"]
