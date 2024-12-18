# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class AdHocExpandMeta(UniversalBaseModel):
    cost: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If enabled, the response will include model host cost tracking. This may increase latency for some model hosts.
    """

    model_name: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If enabled, the response will include the model identifier representing the ML Model invoked by the Prompt.
    """

    usage: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If enabled, the response will include model host usage tracking. This may increase latency for some model hosts.
    """

    finish_reason: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If enabled, the response will include the reason provided by the model for why the execution finished.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
