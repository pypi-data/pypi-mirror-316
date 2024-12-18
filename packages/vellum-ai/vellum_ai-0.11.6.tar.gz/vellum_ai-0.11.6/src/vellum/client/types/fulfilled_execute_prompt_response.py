# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .prompt_execution_meta import PromptExecutionMeta
import pydantic
from .prompt_output import PromptOutput
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class FulfilledExecutePromptResponse(UniversalBaseModel):
    """
    The successful response from the model containing all of the resolved values generated by the prompt.
    """

    meta: typing.Optional[PromptExecutionMeta] = None
    raw: typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]] = pydantic.Field(default=None)
    """
    The subset of the raw response from the model that the request opted into with `expand_raw`.
    """

    execution_id: str = pydantic.Field()
    """
    The ID of the execution.
    """

    state: typing.Literal["FULFILLED"] = "FULFILLED"
    outputs: typing.List[PromptOutput]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
