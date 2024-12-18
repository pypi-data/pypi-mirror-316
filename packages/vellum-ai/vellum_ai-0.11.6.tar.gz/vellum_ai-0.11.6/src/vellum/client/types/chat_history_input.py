# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .chat_message import ChatMessage
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class ChatHistoryInput(UniversalBaseModel):
    """
    A user input representing a list of chat messages
    """

    name: str = pydantic.Field()
    """
    The variable's name, as defined in the deployment.
    """

    type: typing.Literal["CHAT_HISTORY"] = "CHAT_HISTORY"
    value: typing.List[ChatMessage]

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
