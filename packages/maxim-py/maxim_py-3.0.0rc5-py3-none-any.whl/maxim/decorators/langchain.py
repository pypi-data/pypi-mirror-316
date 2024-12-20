from contextvars import ContextVar
from functools import wraps
from typing import Any, Dict, Optional

from ..logger.langchain import MaximLangchainTracer
from ..logger.logger import Logger
from .span import current_span
from .trace import current_logger, current_trace

_langchain_tracer_ctx_var: ContextVar[Optional[MaximLangchainTracer]] = ContextVar(
    "maxim_ctx_langchain_tracer", default=None
)


def langchain_callback() -> Optional[MaximLangchainTracer]:
    return _langchain_tracer_ctx_var.get(None)


def langchain_llm_call(
    logger: Optional[Logger] = None,
    name: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # First check if the logger is available
            maxim_logger = logger
            if maxim_logger is None:
                if current_logger() is None:
                    raise ValueError(
                        "[MaximSDK]: no logger found. either call this function from a @trace decorated function or pass a logger"
                    )
                maxim_logger = current_logger()
            # Here there should be an active span or active trace
            # If none of this is the case then we raise an error
            if current_span() is None and current_trace() is None:
                if maxim_logger.raise_exceptions:
                    raise ValueError(
                        "[MaximSDK]: no trace or span found. either call this function from a @trace or @span decorated function"
                    )
                else:
                    logging.warning(
                        "[MaximSDK]: no trace or span found. either call this function from a @trace or @span decorated function"
                    )
            # This is a valid call
            metadata: Dict[str, Any] = {}
            if current_span() is not None:
                metadata["span_id"] = current_span().id
            elif current_trace() is not None:
                metadata["trace_id"] = current_trace().id
            if tags is not None:
                metadata["generation_tags"] = tags
            if name is not None:
                metadata["generation_name"] = name
            tracer = MaximLangchainTracer(logger=maxim_logger, metadata=metadata)
            token = _langchain_tracer_ctx_var.set(tracer)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                _langchain_tracer_ctx_var.reset(token)

        return wrapper

    return decorator
