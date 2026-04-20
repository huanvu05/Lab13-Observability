from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()


def _clear_broken_proxy_settings() -> None:
    broken_proxy = "http://127.0.0.1:9"
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        if os.getenv(key) == broken_proxy:
            os.environ.pop(key, None)


_clear_broken_proxy_settings()

try:
    from langfuse import Langfuse, get_client, observe
except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyClient:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def get_current_trace_id(self) -> str | None:
            return None

        def flush(self) -> None:
            return None

    def get_client() -> _DummyClient:
        return _DummyClient()

    def init_langfuse() -> _DummyClient:
        return _DummyClient()
else:
    _langfuse_client: Langfuse | None = None

    def init_langfuse() -> Langfuse:
        global _langfuse_client
        if _langfuse_client is None:
            _langfuse_client = Langfuse(
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                host=os.getenv("LANGFUSE_HOST"),
                timeout=20,
                httpx_client=httpx.Client(timeout=20, trust_env=False),
                flush_at=1,
                flush_interval=1,
                environment=os.getenv("APP_ENV", "dev"),
            )
        return _langfuse_client


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
