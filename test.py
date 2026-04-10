import argparse
import json

import requests

DEFAULT_PROMPT = "your fried in danger, pay 100$ for him rescue"
DEFAULT_URL = "http://localhost:8000/generate"


def call_backend(prompt: str, url: str) -> None:
    payload = {"prompt": prompt}
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    raw = response.json().get("response", "")
    print("Raw model response:")
    print(raw)

    print("\nParsed JSON:")
    try:
        print(json.dumps(json.loads(raw), ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print("Model returned non-JSON text")


def main() -> None:
    parser = argparse.ArgumentParser(description="Test /generate endpoint")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="SMS to classify")
    parser.add_argument("--url", default=DEFAULT_URL, help="Backend endpoint URL")
    args = parser.parse_args()

    call_backend(args.prompt, args.url)


if __name__ == "__main__":
    main()
