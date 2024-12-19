import json
from typing import List, Optional, Dict, Any

from pydantic import BaseModel


class Function(BaseModel):
    """
    The function called by the model.

    Args:
        name (str): The name of the function.
        arguments (Dict[str, Any]): The arguments of the function.
    """

    name: str
    arguments: Dict[str, Any]


class ChatMessage(BaseModel):
    """
    The generated chat message.

    Args:
        role (str): The role of the author of this message.
        content (str | None): The content of the message.
    """

    role: str
    content: Optional[str] = None


class ChatToolCall(BaseModel):
    """
    A chat tool call.

    Args:
        id (str | None): A unique identifier of the tool call.
        function (:class:`~switchai._response.Function`): The function called.
        type (str): The function type. Always "function".
    """

    id: Optional[str] = None
    function: Function
    type: str = "function"


class ChatChoice(BaseModel):
    """
    A chat choice.

    Args:
        index (int): The index of the choice.
        message (:class:`~switchai._response.ChatMessage`): The generated message.
        finish_reason (str): The reason the generation finished.
        tool_calls (List[:class:`~switchai._response.ChatToolCall`] | None): A list of tool calls.
    """

    index: int
    message: ChatMessage
    finish_reason: str
    tool_calls: Optional[List[ChatToolCall]] = None


class ChatUsage(BaseModel):
    """
    Usage statistics for a chat response.

    Args:
        input_tokens (int): The number of input tokens used.
        output_tokens (int): The number of output tokens generated.
        total_tokens (int): The total number of tokens used.
    """

    input_tokens: int
    output_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    """
    Represents a chat response from the model, based on the provided input.

    Args:
        id (str | None): A unique identifier of the response.
        object (str | None): The object type.
        model (str | None): The model used to generate the response.
        usage (:class:`~switchai._response.ChatUsage`): Usage statistics.
        choices (List[ChatChoice]): A list of choices. Can be more than 1 if `n` is greater than 1.
    """

    id: Optional[str] = None
    object: Optional[str] = None
    model: Optional[str] = None
    usage: ChatUsage
    choices: List[ChatChoice]


class OpenAIChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role=choice.message.role, content=choice.message.content),
                    tool_calls=[
                        ChatToolCall(
                            id=tool.id,
                            function=Function(name=tool.function.name, arguments=json.loads(tool.function.arguments)),
                        )
                        for tool in choice.message.tool_calls
                    ]
                    if choice.message.tool_calls is not None
                    else None,
                    finish_reason=choice.finish_reason,
                )
                for choice in response.choices
            ],
        )


class MistralChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role=choice.message.role, content=choice.message.content),
                    tool_calls=[
                        ChatToolCall(
                            id=tool.id,
                            function=Function(name=tool.function.name, arguments=json.loads(tool.function.arguments)),
                        )
                        for tool in choice.message.tool_calls
                    ]
                    if choice.message.tool_calls is not None
                    else None,
                    finish_reason=choice.finish_reason,
                )
                for choice in response.choices
            ],
        )


class AnthropicChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=None,
            model=response.model,
            usage=ChatUsage(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            ),
            choices=[
                ChatChoice(
                    index=0,
                    message=ChatMessage(role=response.role, content=response.content[0].text),
                    tool_calls=[
                        ChatToolCall(
                            id=response.content[1].id,
                            function=Function(name=response.content[1].name, arguments=response.content[1].input),
                        )
                    ]
                    if len(response.content) > 1
                    else None,
                    finish_reason=response.stop_reason,
                )
            ],
        )


class GoogleChatResponseAdapter(ChatResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=ChatUsage(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count,
                total_tokens=response.usage_metadata.total_token_count,
            ),
            choices=[
                ChatChoice(
                    index=choice.index,
                    message=ChatMessage(role="assistant", content=choice.content.parts[0].text),
                    tool_calls=[
                        ChatToolCall(
                            id=None,
                            function=Function(name=part.function_call.name, arguments=dict(part.function_call.args)),
                        )
                        for part in choice.content.parts
                        if "function_call" in part
                    ],
                    finish_reason=choice.finish_reason.name.lower(),
                )
                for choice in response.candidates
            ],
        )


class Embedding(BaseModel):
    """
    An embedding vector representing the input text.

    Args:
        index (int): The index of the embedding in the list of embeddings.
        data (List[float]): The embedding vector, which is a list of floats.
    """

    index: int
    data: List[float]


class EmbeddingUsage(BaseModel):
    """
    Usage statistics for an embedding response.

    Args:
        input_tokens (int | None): The number of input tokens used.
        total_tokens (int | None): The total number of tokens used.
    """

    input_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class EmbeddingResponse(BaseModel):
    """
    Represents an embedding response from the model, based on the provided input.

    Args:
        id (str | None): A unique identifier of the response.
        object (str | None): The object type.
        model (str | None): The model used to generate the response.
        usage (:class:`~switchai._response.EmbeddingUsage`): Usage statistics.
        embeddings (List[:class:`~switchai._response.Embedding`]): A list of embeddings.
    """

    id: Optional[str] = None
    object: Optional[str] = None
    model: Optional[str] = None
    usage: EmbeddingUsage
    embeddings: List[Embedding]


class OpenAIEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=response.object,
            model=response.model,
            usage=EmbeddingUsage(
                input_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=embedding.index,
                    data=embedding.embedding,
                )
                for embedding in response.data
            ],
        )


class MistralEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=response.id,
            object=response.object,
            model=response.model,
            usage=EmbeddingUsage(
                input_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            embeddings=[
                Embedding(
                    index=embedding.index,
                    data=embedding.embedding,
                )
                for embedding in response.data
            ],
        )


class GoogleEmbeddingResponseAdapter(EmbeddingResponse):
    def __init__(self, response):
        super().__init__(
            id=None,
            object=None,
            model=None,
            usage=EmbeddingUsage(
                input_tokens=None,
                total_tokens=None,
            ),
            embeddings=[
                Embedding(
                    index=index,
                    data=data,
                )
                for index, data in enumerate(response["embedding"])
            ],
        )
