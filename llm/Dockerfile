FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY agent-server.py .

EXPOSE 8080
CMD ["python", "agent-server.py"]