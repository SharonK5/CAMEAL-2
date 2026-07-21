# kernel/providers/llm/llm_provider.py
"""
LLM provider abstraction.
"""

from abc import abstractmethod
from typing import Any, List, Dict, Optional, AsyncIterator, Iterator

from ..base.provider import Provider


class LLMProvider(Provider):
    """
    Base interface for language model providers.

    LLM providers abstract access to various language model services:
        - Local models (Ollama, llama.cpp, etc.)
        - Cloud APIs (OpenAI, Anthropic, Cohere, etc.)
        - Enterprise services (Azure OpenAI, Google Vertex AI, etc.)

    All LLM providers must support:
        - Generation (synchronous and streaming)
        - Chat completion
        - Model identification (name, version)
        - Configuration (temperature, max_tokens, etc.)
    """

    @abstractmethod
    def get(self) -> Any:
        """Return the underlying LLM client."""
        pass

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from a prompt.

        Args:
            prompt: The input prompt.
            **kwargs: Generation parameters (temperature, max_tokens, etc.).

        Returns:
            The generated text response.

        Raises:
            ProviderError: If generation fails.
        """
        pass

    @abstractmethod
    def stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """
        Stream a response from a prompt.

        Args:
            prompt: The input prompt.
            **kwargs: Generation parameters.

        Yields:
            Chunks of the generated response (strings).

        Raises:
            ProviderError: If streaming fails.
        """
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Chat completion.

        Args:
            messages: List of message dicts with "role" and "content".
                      Example: [{"role": "user", "content": "Hello"}]
            **kwargs: Generation parameters.

        Returns:
            The assistant's response text.

        Raises:
            ProviderError: If chat completion fails.
        """
        pass

    @abstractmethod
    def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
        """
        Stream chat completion.

        Args:
            messages: List of message dicts with "role" and "content".
            **kwargs: Generation parameters.

        Yields:
            Chunks of the assistant's response.

        Raises:
            ProviderError: If streaming fails.
        """
        pass

    @abstractmethod
    def model_name(self) -> str:
        """
        Return the name of the underlying model.

        Returns:
            The model name (e.g., "llama2", "gpt-4", "claude-3").
        """
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Return True if the provider supports streaming."""
        pass
