
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/
COPY sql/ ./sql/
COPY data/ ./data/

CMD ["python", "-u", "src/etl_pipeline.py"]
