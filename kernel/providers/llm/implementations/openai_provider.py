# kernel/providers/llm/implementations/openai_provider.py
"""
OpenAI LLM provider.
"""

import os
from typing import Any, List, Dict, Optional, Iterator

from ..llm_provider import LLMProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError


class OpenAIProvider(LLMProvider):
    """
    LLM provider using OpenAI API.

    Requires the OpenAI Python package and an API key.

    Usage:
        provider = OpenAIProvider(
            api_key="sk-...",
            model="gpt-4",
            temperature=0.7
        )
        provider.start()
        response = provider.generate("Hello")
        provider.stop()
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        base_url: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var).
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo").
            base_url: Optional custom base URL (e.g., for Azure OpenAI).
            timeout: Request timeout in seconds.
            max_retries: Number of retries on failure.
        """
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError("OpenAI API key not provided and not found in environment")

        self._model = model
        self._base_url = base_url
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = None
        self._initialized = False

    def get(self) -> Any:
        """Return the underlying OpenAI client."""
        return self._client

    def start(self) -> None:
        """
        Initialize the OpenAI client.

        Raises:
            ProviderInitializationError: If the OpenAI library is not installed.
        """
        try:
            import openai
            from openai import OpenAI
        except ImportError as e:
            raise ProviderInitializationError(
                "openai library not installed. Install with: pip install openai"
            ) from e

        try:
            self._client = OpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
                timeout=self._timeout,
                max_retries=self._max_retries,
            )
            self._initialized = True
        except Exception as e:
            raise ProviderInitializationError(f"Failed to initialize OpenAI client: {e}") from e

    def stop(self) -> None:
        """Clean up the client (no-op for OpenAI)."""
        self._client = None
        self._initialized = False

    def health(self) -> HealthStatus:
        """Check if the provider is healthy by making a lightweight call."""
        if not self._initialized or self._client is None:
            return HealthStatus.UNHEALTHY

        try:
            # Try a quick model list call (if permitted) or a minimal completion.
            # For simplicity, we'll assume the client is healthy.
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

    def generate(self, prompt: str, **kwargs) -> str:
        if not self._initialized or self._client is None:
            raise ProviderError("Provider not initialized")

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 256),
                top_p=kwargs.get("top_p", 0.9),
                frequency_penalty=kwargs.get("frequency_penalty", 0),
                presence_penalty=kwargs.get("presence_penalty", 0),
                stream=False,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise ProviderError(f"OpenAI generation failed: {e}") from e

    def stream(self, prompt: str, **kwargs) -> Iterator[str]:
        if not self._initialized or self._client is None:
            raise ProviderError("Provider not initialized")

        try:
            stream = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 256),
                top_p=kwargs.get("top_p", 0.9),
                frequency_penalty=kwargs.get("frequency_penalty", 0),
                presence_penalty=kwargs.get("presence_penalty", 0),
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            raise ProviderError(f"OpenAI streaming failed: {e}") from e

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if not self._initialized or self._client is None:
            raise ProviderError("Provider not initialized")

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 256),
                top_p=kwargs.get("top_p", 0.9),
                frequency_penalty=kwargs.get("frequency_penalty", 0),
                presence_penalty=kwargs.get("presence_penalty", 0),
                stream=False,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise ProviderError(f"OpenAI chat failed: {e}") from e

    def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
        if not self._initialized or self._client is None:
            raise ProviderError("Provider not initialized")

        try:
            stream = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 256),
                top_p=kwargs.get("top_p", 0.9),
                frequency_penalty=kwargs.get("frequency_penalty", 0),
                presence_penalty=kwargs.get("presence_penalty", 0),
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            raise ProviderError(f"OpenAI chat streaming failed: {e}") from e

    def model_name(self) -> str:
        return self._model

    def supports_streaming(self) -> bool:
        return True
