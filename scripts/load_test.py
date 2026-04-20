import argparse
import concurrent.futures
import json
import time
from pathlib import Path

import httpx

BASE_URL = "http://127.0.0.1:8000"
QUERIES = Path("data/test_queries.jsonl")


def load_payloads(path: Path) -> list[dict]:
    raw_text = path.read_text(encoding="utf-8").strip()
    if not raw_text:
        return []

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed = [json.loads(line) for line in raw_text.splitlines() if line.strip()]

    if isinstance(parsed, dict):
        records = [parsed]
    else:
        records = list(parsed)

    return [normalize_payload(record, index) for index, record in enumerate(records, start=1)]


def normalize_payload(record: dict, index: int) -> dict:
    if "message" in record and "session_id" in record:
        return record

    user_id = str(record.get("user_id") or f"u_test_{index:02d}")
    feature = str(record.get("feature") or "qa")
    session_id = str(record.get("session_id") or f"s_test_{index:02d}")
    event = str(record.get("event") or "agent_response")
    level = str(record.get("level") or "INFO").upper()
    latency_ms = record.get("latency_ms", "unknown")
    model = str(record.get("model") or "unknown")
    tokens_in = record.get("tokens_in", "unknown")
    tokens_out = record.get("tokens_out", "unknown")
    cost_usd = record.get("cost_usd", "unknown")
    correlation_id = str(record.get("correlation_id") or f"req-test-{index:03d}")

    if level == "ERROR":
        message = (
            f"Investigate this incident and explain the likely root cause. "
            f"Event={event}. Correlation ID={correlation_id}. Feature={feature}. "
            f"Model={model}. Latency={latency_ms}ms. Tokens in/out={tokens_in}/{tokens_out}. "
            f"Cost=${cost_usd}. What should the team check first?"
        )
        normalized_feature = "qa"
    elif level == "WARN":
        message = (
            f"Summarize the operational risk in this warning event. "
            f"Event={event}. Correlation ID={correlation_id}. Feature={feature}. "
            f"Model={model}. Latency={latency_ms}ms. Tokens in/out={tokens_in}/{tokens_out}. "
            f"Cost=${cost_usd}. Keep the summary short and actionable."
        )
        normalized_feature = "summary"
    else:
        message = (
            f"Analyze this successful request and explain what it tells us about system behavior. "
            f"Event={event}. Correlation ID={correlation_id}. Feature={feature}. "
            f"Model={model}. Latency={latency_ms}ms. Tokens in/out={tokens_in}/{tokens_out}. "
            f"Cost=${cost_usd}. Give a concise answer."
        )
        normalized_feature = "qa"

    return {
        "user_id": user_id,
        "session_id": session_id,
        "feature": normalized_feature,
        "message": message,
    }


def send_request(client: httpx.Client, payload: dict) -> None:
    try:
        start = time.perf_counter()
        r = client.post(f"{BASE_URL}/chat", json=payload)
        latency = (time.perf_counter() - start) * 1000
        print(f"[{r.status_code}] {r.json().get('correlation_id')} | {payload['feature']} | {latency:.1f}ms")
    except Exception as e:
        print(f"Error: {e}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent requests")
    parser.add_argument("--file", type=Path, default=QUERIES, help="Path to JSONL or JSON input data")
    args = parser.parse_args()

    payloads = load_payloads(args.file)
    
    with httpx.Client(timeout=30.0) as client:
        if args.concurrency > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                futures = [executor.submit(send_request, client, payload) for payload in payloads]
                concurrent.futures.wait(futures)
        else:
            for payload in payloads:
                send_request(client, payload)


if __name__ == "__main__":
    main()
