import logging
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID, uuid4

# Use LangChain features
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

from ...expiringKeyValueStore import ExpiringKeyValueStore
from ...logger.components.generation import GenerationConfig, GenerationError
from ...logger.components.retrieval import RetrievalConfig
from ...logger.components.trace import TraceConfig
from ...logger.logger import Logger
from .utils import (parse_langchain_llm_error, parse_langchain_llm_result,
                    parse_langchain_messages,
                    parse_langchain_model_and_provider,
                    parse_langchain_model_parameters, parse_langchain_provider)

logger = logging.getLogger("MaximSDK")

# 20 minutes
DEFAULT_TIMEOUT = 60 * 20


class MaximLangchainTracer(BaseCallbackHandler):
    """A callback handler that logs langchain outputs to Maxim logger

    Args:
        logger: Logger: Maxim Logger instance to log outputs
    """

    def __init__(self, logger: Logger, metadata: Optional[Dict[str, Any]]) -> None:
        """Initializes the Langchain Tracer
        Args:
            logger: Logger: Maxim Logger instance to log outputs
        """
        super().__init__()
        self.logger = logger
        self.generations = ExpiringKeyValueStore()
        self.retrievals = ExpiringKeyValueStore()
        self.metadata_store = ExpiringKeyValueStore()
        self.metadata = None
        if metadata is not None:
            self._validate_maxim_metadata(metadata)
            self.metadata = metadata

    def _validate_maxim_metadata(self, metadata: Dict[str, Any]):
        if metadata is None:
            return
        id_keys = ["session_id", "trace_id", "span_id"]
        present_keys = [key for key in id_keys if key in metadata]
        if len(present_keys) > 1:
            raise ValueError(
                f"Multiple keys found in metadata: {present_keys}. You can pass only one of these."
            )
        valid_keys = [
            "session_id",
            "trace_id",
            "span_id",
            "generation_tags",
            "retrieval_tags",
            "trace_tags",
            "retrieval_name",
            "trace_name",
            "generation_name",
        ]
        invalid_keys = [key for key in metadata if key not in valid_keys]
        if len(invalid_keys) > 0:
            raise ValueError(
                f"Invalid keys found in metadata: {invalid_keys}. Valid keys are {valid_keys}"
            )

    def _get_container(self, run_id: UUID):
        maxim_metadata = self.metadata_store.get(str(run_id))
        if maxim_metadata is not None:
            span_id = maxim_metadata.get("span_id", None)
            if span_id is not None:
                return "span", span_id
            session_id = maxim_metadata.get("session_id", None)
            if session_id is not None:
                return "session", session_id
            trace_id = maxim_metadata.get("trace_id", None)
            if trace_id is not None:
                return "trace", trace_id
        return "local_trace", str(run_id)

    # LLM callbacks

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[Langchain] on_llm_start called")
        model, model_parameters = parse_langchain_model_parameters(**kwargs)
        provider = parse_langchain_provider(serialized)
        model, provider = parse_langchain_model_and_provider(model, provider)
        messages = parse_langchain_messages(prompts)
        generation_id = str(uuid4())
        generation_name = None
        generation_tags = None
        trace_tags = None

        if metadata is not None and metadata.get("maxim", None) is not None:
            self._validate_maxim_metadata(metadata.get("maxim", None))
            self.metadata_store.set(
                str(run_id), metadata.get("maxim", None), DEFAULT_TIMEOUT
            )
            trace_tags = metadata.get("maxim", {}).get("trace_tags", None)
            generation_name = metadata.get("maxim", {}).get("generation_name", None)
            generation_tags = metadata.get("maxim", {}).get("generation_tags", None)
        elif self.metadata is not None:
            self.metadata_store.set(str(run_id), self.metadata, DEFAULT_TIMEOUT)
            trace_tags = self.metadata.get("trace_tags", None)
            generation_name = self.metadata.get("generation_name", None)
            generation_tags = self.metadata.get("generation_tags", None)

        generation_config = GenerationConfig(
            id=generation_id,
            name=generation_name,
            provider=provider,
            model=model,
            messages=messages,
            model_parameters=model_parameters,
            tags=generation_tags,
        )

        self.generations.set(str(run_id), generation_id, DEFAULT_TIMEOUT)

        container, container_id = self._get_container(run_id)

        if container == "span":
            self.logger.span_generation(container_id, generation_config)
        elif container == "trace":
            self.logger.trace_generation(container_id, generation_config)
        elif container == "session":
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.session_trace(
                container_id,
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags),
            )
            trace.generation(generation_config)
        else:
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.trace(
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags)
            )
            trace.generation(generation_config)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        logger.debug(f"[Langchain] on_llm_end called")
        run_id = kwargs.get("run_id", None)
        if run_id is not None:
            result = parse_langchain_llm_result(response)
            generation_id = self.generations.get(str(run_id))
            if generation_id is not None:
                container, container_id = self._get_container(run_id)
                self.logger.generation_result(generation_id, result)
                if container == "local_trace":
                    self.logger.trace_end(container_id)

    # Retrieval callbacks

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[Langchain] on_retriever_start called")
        """Run when Retriever starts running."""
        container, container_id = self._get_container(run_id)
        retrieval_id = str(uuid4())
        retrieval_config = RetrievalConfig(id=retrieval_id)
        if container == "span":
            retrieval = self.logger.span_retrieval(
                container_id, config=retrieval_config
            )
            retrieval.input(query)
        elif container == "trace":
            retrieval = self.logger.trace_retrieval(
                container_id, config=retrieval_config
            )
            retrieval.input(query)
        elif container == "session":
            trace = self.logger.session_trace(container_id, TraceConfig(id=str(run_id)))
            retrieval = trace.retrieval(retrieval_config)
            retrieval.input(query)
        else:
            retrieval = self.logger.trace_retrieval(
                str(run_id), config=retrieval_config
            )
            retrieval.input(query)

    def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[Langchain] on_retriever_end called")
        trace_id = str(run_id)
        retrieval_id = self.retrievals.get(trace_id)
        if retrieval_id is not None:
            self.logger.retrieval_output(retrieval_id, documents)

    # ChatModel callbacks

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug(f"[Langchain] on_chat_model_start called")
        model, model_parameters = parse_langchain_model_parameters(**kwargs)
        provider = parse_langchain_provider(serialized)
        model, provider = parse_langchain_model_and_provider(model, provider)
        maxim_messages = parse_langchain_messages(messages)
        run_id = kwargs.get("run_id", None)
        generation_id = str(uuid4())
        generation_name = None
        generation_tags = None
        trace_tags = None

        if metadata is not None:
            self._validate_maxim_metadata(metadata.get("maxim", None))
            self.metadata_store.set(
                str(run_id), metadata.get("maxim", None), DEFAULT_TIMEOUT
            )
            trace_tags = metadata.get("maxim", {}).get("trace_tags", None)
            generation_name = metadata.get("maxim", {}).get("generation_name", None)
            generation_tags = metadata.get("maxim", {}).get("generation_tags", None)
        elif self.metadata is not None:
            self.metadata_store.set(str(run_id), self.metadata, DEFAULT_TIMEOUT)
            trace_tags = self.metadata.get("trace_tags", None)
            generation_name = self.metadata.get("generation_name", None)
            generation_tags = self.metadata.get("generation_tags", None)

        generation_config = GenerationConfig(
            id=generation_id,
            name=generation_name,
            provider=provider,
            model=model,
            messages=maxim_messages,
            model_parameters=model_parameters,
            tags=generation_tags,
        )
        self.generations.set(str(run_id), generation_id, DEFAULT_TIMEOUT)

        container, container_id = self._get_container(run_id)

        if container == "span":
            self.logger.span_generation(container_id, generation_config)
        elif container == "trace":
            self.logger.trace_generation(container_id, generation_config)
        elif container == "session":
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.session_trace(
                container_id,
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags),
            )
            trace.generation(generation_config)
        else:
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.trace(
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags)
            )
            trace.generation(generation_config)

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        logger.debug(f"[Langchain] on_llm_error called")
        run_id = kwargs.get("run_id", None)
        if run_id is not None:
            generation_id = self.generations.get(str(run_id))
            if generation_id is not None:
                container, container_id = self._get_container(run_id)
                generation_error = parse_langchain_llm_error(error)
                self.logger.generation_error(generation_id, generation_error)
                if container == "local_trace":
                    self.logger.trace_end(container_id)

    # Chain callbacks

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        raise ValueError(
            "To trace chains using Maxim, attach MaximLangchainTracer to the LLM instead. We automatically group all LLM calls in a chain under one trace."
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        pass

    def on_chain_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        pass

    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        logger.warning(f"[MaximSDK] Agent actions not supported")

    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        logger.warning(f"[MaximSDK] Agent finishes not supported")

    # Tool callbacks

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        logger.error(f"[MaximSDK] Tool not supported")

    def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
        logger.error(f"[MaximSDK] Tool not supported")

    def on_tool_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        logger.error(f"[MaximSDK] Tool not supported")

    def on_text(self, text: str, **kwargs: Any) -> Any:
        pass
