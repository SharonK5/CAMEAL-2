# kernel/providers/llm/implementations/ollama_provider.py
"""
Ollama LLM provider.

Ollama provides local LLM serving with a simple API.
"""

import json
import requests
from typing import Any, List, Dict, Optional, Iterator
import logging

from ..llm_provider import LLMProvider
from kernel.lifecycle import HealthStatus
from ...base.exceptions import ProviderInitializationError, ProviderError

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    """
    LLM provider using Ollama API.

    Ollama runs locally and supports many open-source models:
        - llama2, llama3
        - mistral, mixtral
        - phi, gemma
        - and more

    Requirements:
        - Ollama installed and running
        - Model pulled (e.g., `ollama pull llama2`)

    Usage:
        provider = OllamaProvider(model="llama2")
        provider.start()
        response = provider.generate("Hello, how are you?")
        provider.stop()
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama2",
        timeout: int = 60,
    ) -> None:
        """
        Initialize the Ollama provider.

        Args:
            base_url: Ollama API endpoint.
            model: Model name (must be pulled locally).
            timeout: Request timeout in seconds.
        """
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout
        self._session = None
        self._initialized = False

    def get(self) -> Any:
        """Return the underlying requests.Session."""
        return self._session

    def start(self) -> None:
        """
        Initialize the HTTP session and check connectivity.

        Raises:
            ProviderInitializationError: If Ollama is not reachable or model is not available.
        """
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})

        # Check connectivity
        try:
            response = self._session.get(
                f"{self._base_url}/api/tags",
                timeout=5
            )
            if response.status_code != 200:
                raise ProviderInitializationError(
                    f"Ollama API returned {response.status_code}: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise ProviderInitializationError(
                f"Failed to connect to Ollama at {self._base_url}: {e}"
            ) from e

        # Check if model exists
        try:
            tags = response.json().get("models", [])
            model_exists = any(m.get("name") == self._model for m in tags)
            if not model_exists:
                logger.warning(
                    f"Model '{self._model}' not found locally. "
                    f"Available models: {[m.get('name') for m in tags]}"
                )
                # We'll still allow it; generation will fail if not available.
        except Exception:
            pass

        self._initialized = True
        logger.info(f"Ollama provider initialized with model '{self._model}'")

    def stop(self) -> None:
        """Close the HTTP session."""
        if self._session:
            self._session.close()
        self._session = None
        self._initialized = False

    def health(self) -> HealthStatus:
        """
        Check health by calling the Ollama API.

        Returns:
            HealthStatus.HEALTHY if Ollama is reachable and model is available.
            HealthStatus.UNHEALTHY otherwise.
        """
        if not self._initialized or self._session is None:
            return HealthStatus.UNHEALTHY

        try:
            response = self._session.get(
                f"{self._base_url}/api/tags",
                timeout=3
            )
            if response.status_code != 200:
                return HealthStatus.UNHEALTHY

            tags = response.json().get("models", [])
            model_exists = any(m.get("name") == self._model for m in tags)
            if not model_exists:
                return HealthStatus.DEGRADED  # Model missing but Ollama is up
            return HealthStatus.HEALTHY
        except Exception:
            return HealthStatus.UNHEALTHY

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the model.

        Args:
            prompt: The input prompt.
            **kwargs: Override generation parameters (temperature, max_tokens, etc.).

        Returns:
            The generated text.

        Raises:
            ProviderError: If generation fails.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "top_k": kwargs.get("top_k", 40),
                "num_predict": kwargs.get("max_tokens", 256),
                "repeat_penalty": kwargs.get("repeat_penalty", 1.1),
            },
        }
        try:
            response = self._session.post(
                f"{self._base_url}/api/generate",
                json=payload,
                timeout=self._timeout,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            raise ProviderError(f"Ollama generation failed: {e}") from e

    def stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """
        Stream a response from the model.

        Args:
            prompt: The input prompt.
            **kwargs: Generation parameters.

        Yields:
            Chunks of the generated response.

        Raises:
            ProviderError: If streaming fails.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "top_k": kwargs.get("top_k", 40),
                "num_predict": kwargs.get("max_tokens", 256),
                "repeat_penalty": kwargs.get("repeat_penalty", 1.1),
            },
        }
        try:
            with self._session.post(
                f"{self._base_url}/api/generate",
                json=payload,
                timeout=self._timeout,
                stream=True,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        content = chunk.get("response", "")
                        if content:
                            yield content
                        if chunk.get("done", False):
                            break
        except requests.exceptions.RequestException as e:
            raise ProviderError(f"Ollama streaming failed: {e}") from e

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Chat completion.

        Args:
            messages: List of message dicts.
            **kwargs: Generation parameters.

        Returns:
            The assistant's response.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "top_k": kwargs.get("top_k", 40),
                "num_predict": kwargs.get("max_tokens", 256),
                "repeat_penalty": kwargs.get("repeat_penalty", 1.1),
            },
        }
        try:
            response = self._session.post(
                f"{self._base_url}/api/chat",
                json=payload,
                timeout=self._timeout,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            raise ProviderError(f"Ollama chat failed: {e}") from e

    def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
        """
        Stream chat completion.

        Args:
            messages: List of message dicts.
            **kwargs: Generation parameters.

        Yields:
            Chunks of the assistant's response.
        """
        if not self._initialized or self._session is None:
            raise ProviderError("Provider not initialized")

        payload = {
            "model": self._model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "top_k": kwargs.get("top_k", 40),
                "num_predict": kwargs.get("max_tokens", 256),
                "repeat_penalty": kwargs.get("repeat_penalty", 1.1),
            },
        }
        try:
            with self._session.post(
                f"{self._base_url}/api/chat",
                json=payload,
                timeout=self._timeout,
                stream=True,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield content
                        if chunk.get("done", False):
                            break
        except requests.exceptions.RequestException as e:
            raise ProviderError(f"Ollama chat streaming failed: {e}") from e

    def model_name(self) -> str:
        return self._model

    def supports_streaming(self) -> bool:
        return True
