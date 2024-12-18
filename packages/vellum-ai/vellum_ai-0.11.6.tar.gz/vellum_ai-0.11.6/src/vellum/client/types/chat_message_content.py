# This file was auto-generated by Fern from our API Definition.

import typing
from .string_chat_message_content import StringChatMessageContent
from .function_call_chat_message_content import FunctionCallChatMessageContent
from .array_chat_message_content import ArrayChatMessageContent
from .image_chat_message_content import ImageChatMessageContent
from .audio_chat_message_content import AudioChatMessageContent

ChatMessageContent = typing.Union[
    StringChatMessageContent,
    FunctionCallChatMessageContent,
    ArrayChatMessageContent,
    ImageChatMessageContent,
    AudioChatMessageContent,
]
