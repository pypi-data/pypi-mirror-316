# This file was auto-generated by Fern from our API Definition.

import typing
from .string_chat_message_content_request import StringChatMessageContentRequest
from .function_call_chat_message_content_request import FunctionCallChatMessageContentRequest
from .array_chat_message_content_request import ArrayChatMessageContentRequest
from .image_chat_message_content_request import ImageChatMessageContentRequest
from .audio_chat_message_content_request import AudioChatMessageContentRequest

ChatMessageContentRequest = typing.Union[
    StringChatMessageContentRequest,
    FunctionCallChatMessageContentRequest,
    ArrayChatMessageContentRequest,
    ImageChatMessageContentRequest,
    AudioChatMessageContentRequest,
]
