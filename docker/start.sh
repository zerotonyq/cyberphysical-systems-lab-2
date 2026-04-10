#!/usr/bin/env bash
set -euo pipefail

ollama serve &

# Wait until Ollama API is ready.
until curl -fsS http://127.0.0.1:11434/api/tags > /dev/null; do
  sleep 1
done

# Keep the required model exactly the same.
if ! ollama list | awk '{print $1}' | grep -qx 'qwen2.5:0.5b'; then
  ollama pull qwen2.5:0.5b
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
