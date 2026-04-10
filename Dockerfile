FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    zstd \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY docker/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000
EXPOSE 11434

CMD ["/app/start.sh"]
