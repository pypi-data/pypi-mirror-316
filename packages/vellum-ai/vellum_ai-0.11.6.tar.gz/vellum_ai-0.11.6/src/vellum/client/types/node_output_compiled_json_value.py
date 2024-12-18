# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .workflow_node_result_event_state import WorkflowNodeResultEventState
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class NodeOutputCompiledJsonValue(UniversalBaseModel):
    """
    An output returned by a node that is of type JSON.
    """

    type: typing.Literal["JSON"] = "JSON"
    value: typing.Optional[typing.Any] = None
    node_output_id: str
    state: typing.Optional[WorkflowNodeResultEventState] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
