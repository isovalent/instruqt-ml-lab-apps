# ../base/Dockerfile is the base image with Python and PyTorch installed
FROM mnist:base

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY main.py .

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 5000

# Use exec form for better signal handling
CMD ["python", "main.py"]