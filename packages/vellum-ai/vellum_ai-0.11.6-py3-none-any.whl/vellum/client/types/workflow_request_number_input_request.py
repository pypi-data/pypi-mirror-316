# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class WorkflowRequestNumberInputRequest(UniversalBaseModel):
    """
    The input for a number variable in a Workflow.
    """

    name: str = pydantic.Field()
    """
    The variable's name, as defined in the Workflow.
    """

    type: typing.Literal["NUMBER"] = "NUMBER"
    value: float

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
