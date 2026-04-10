# SMS Spam Classifier

FastAPI-приложение с одним эндпоинтом `/generate`, который проксирует запрос в Ollama для классификации SMS на spam/not spam.

Модель: `qwen2.5:0.5b`

## Запуск

```bash
docker build -t image:version .
```

В `docker-compose.yaml` указать:

```yaml
image: image:version
```

```bash
docker compose up -d
```

## API

### POST `/generate`

Request body:

```json
{
  "prompt": "your text message"
}
```

Response body:

```json
{
  "response": "{\"is_spam\": true/false, \"spam_topic\": \"lottery|phishing|ads|scam|\"}"
}
```

## Примеры вызова

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello my dear friend!"}'
```

```bash
python test.py
```

```bash
python test.py --prompt "we have some present for you, pick it up at http://verystrangelink.com"
```

```bash
python test.py --url "http://127.0.0.1:8000/generate" --prompt "Good luck at your new job!"
```

## Swagger

`http://localhost:8000/docs`
