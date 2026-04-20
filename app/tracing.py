from __future__ import annotations

import os
from typing import Any

try:
    # Langfuse >=3: observe và client API (không còn package decorators)
    from langfuse import get_client, observe

    class _LangfuseContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            get_client().update_current_trace(**kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            client = get_client()
            usage_details = kwargs.pop("usage_details", None)
            if usage_details is not None:
                client.update_current_generation(usage_details=usage_details, **kwargs)
            else:
                client.update_current_span(**kwargs)

    langfuse_context = _LangfuseContext()
except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
