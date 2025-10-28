FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && pip install --no-cache-dir -r requirements.txt --index-url https://download.pytorch.org/whl/cpu \
    && apt-get purge -y gcc g++ && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*