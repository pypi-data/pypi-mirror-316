# This file was auto-generated by Fern from our API Definition.

import typing
from .fulfilled_execute_prompt_response import FulfilledExecutePromptResponse
from .rejected_execute_prompt_response import RejectedExecutePromptResponse

ExecutePromptResponse = typing.Union[FulfilledExecutePromptResponse, RejectedExecutePromptResponse]
