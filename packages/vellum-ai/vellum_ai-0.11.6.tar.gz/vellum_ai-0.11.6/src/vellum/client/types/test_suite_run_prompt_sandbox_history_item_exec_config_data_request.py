# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class TestSuiteRunPromptSandboxHistoryItemExecConfigDataRequest(UniversalBaseModel):
    history_item_id: str = pydantic.Field()
    """
    The ID of the Prompt Sandbox History Item that the Test Suite will run against.
    """

    prompt_variant_id: str = pydantic.Field()
    """
    The ID of the Prompt Variant within the Prompt Sandbox History Item that you'd like to run the Test Suite against.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
