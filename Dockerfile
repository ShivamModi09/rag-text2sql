# Stage 1: Build Stage
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# Install CPU-only versions to drop image size by ~1.5GB
RUN pip install --user --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# Stage 2: Database Stage
FROM mysql:8.0 AS data-packer
COPY ./data/init.sql /docker-entrypoint-initdb.d/init.sql

# Stage 3: Final Stage 
FROM python:3.11-slim
WORKDIR /app
# Only copy the installed packages from the builder
COPY --from=builder /root/.local /root/.local
COPY app.py frontend.py ./
COPY src/ ./src/

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0"]
