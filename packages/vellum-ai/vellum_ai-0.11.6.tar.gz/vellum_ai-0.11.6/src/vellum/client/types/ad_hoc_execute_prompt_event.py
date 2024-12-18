# This file was auto-generated by Fern from our API Definition.

import typing
from .initiated_ad_hoc_execute_prompt_event import InitiatedAdHocExecutePromptEvent
from .streaming_ad_hoc_execute_prompt_event import StreamingAdHocExecutePromptEvent
from .fulfilled_ad_hoc_execute_prompt_event import FulfilledAdHocExecutePromptEvent
from .rejected_ad_hoc_execute_prompt_event import RejectedAdHocExecutePromptEvent

AdHocExecutePromptEvent = typing.Union[
    InitiatedAdHocExecutePromptEvent,
    StreamingAdHocExecutePromptEvent,
    FulfilledAdHocExecutePromptEvent,
    RejectedAdHocExecutePromptEvent,
]
