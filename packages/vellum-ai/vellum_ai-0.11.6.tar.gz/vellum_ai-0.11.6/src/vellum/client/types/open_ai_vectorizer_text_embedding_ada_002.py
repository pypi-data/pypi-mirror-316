# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
from .open_ai_vectorizer_config import OpenAiVectorizerConfig
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class OpenAiVectorizerTextEmbeddingAda002(UniversalBaseModel):
    """
    OpenAI vectorizer for text-embedding-ada-002.
    """

    config: OpenAiVectorizerConfig
    model_name: typing.Literal["text-embedding-ada-002"] = "text-embedding-ada-002"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
