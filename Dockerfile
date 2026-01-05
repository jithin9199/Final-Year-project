FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY Frontend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY Frontend ./

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run streamlit
CMD streamlit run --server.port=8501 --server.address=0.0.0.0 app.py
