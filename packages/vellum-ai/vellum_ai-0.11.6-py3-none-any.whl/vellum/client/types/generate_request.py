# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .chat_message_request import ChatMessageRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class GenerateRequest(UniversalBaseModel):
    input_values: typing.Dict[str, typing.Optional[typing.Any]] = pydantic.Field()
    """
    Key/value pairs for each template variable defined in the deployment's prompt.
    """

    chat_history: typing.Optional[typing.List[ChatMessageRequest]] = pydantic.Field(default=None)
    """
    Optionally provide a list of chat messages that'll be used in place of the special chat_history variable, if included in the prompt.
    """

    external_ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Optionally include a unique identifier for each generation, as represented outside of Vellum. Note that this should generally be a list of length one.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
