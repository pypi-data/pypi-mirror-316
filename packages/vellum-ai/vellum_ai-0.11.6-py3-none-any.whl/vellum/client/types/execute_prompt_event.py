# This file was auto-generated by Fern from our API Definition.

import typing
from .initiated_execute_prompt_event import InitiatedExecutePromptEvent
from .streaming_execute_prompt_event import StreamingExecutePromptEvent
from .fulfilled_execute_prompt_event import FulfilledExecutePromptEvent
from .rejected_execute_prompt_event import RejectedExecutePromptEvent

ExecutePromptEvent = typing.Union[
    InitiatedExecutePromptEvent, StreamingExecutePromptEvent, FulfilledExecutePromptEvent, RejectedExecutePromptEvent
]
