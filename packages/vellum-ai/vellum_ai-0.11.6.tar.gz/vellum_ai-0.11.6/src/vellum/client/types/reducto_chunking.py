# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .reducto_chunker_config import ReductoChunkerConfig
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ReductoChunking(UniversalBaseModel):
    """
    Reducto chunking
    """

    chunker_name: typing.Literal["reducto-chunker"] = "reducto-chunker"
    chunker_config: typing.Optional[ReductoChunkerConfig] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
