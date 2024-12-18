# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .finish_reason_enum import FinishReasonEnum
from .normalized_log_probs import NormalizedLogProbs
from .vellum_variable_type import VellumVariableType
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class EnrichedNormalizedCompletion(UniversalBaseModel):
    id: str = pydantic.Field()
    """
    The Vellum-generated ID of the completion.
    """

    external_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The external ID that was originally provided along with the generation request, which uniquely identifies this generation in an external system.
    """

    text: str = pydantic.Field()
    """
    The text generated by the LLM.
    """

    finish_reason: typing.Optional[FinishReasonEnum] = pydantic.Field(default=None)
    """
    The reason the generation finished.
    
    - `LENGTH` - LENGTH
    - `STOP` - STOP
    - `UNKNOWN` - UNKNOWN
    """

    logprobs: typing.Optional[NormalizedLogProbs] = pydantic.Field(default=None)
    """
    The logprobs of the completion. Only present if specified in the original request options.
    """

    model_version_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The ID of the model version used to generate this completion.
    """

    prompt_version_id: str
    type: typing.Optional[VellumVariableType] = None
    deployment_release_tag: str
    model_name: str

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
