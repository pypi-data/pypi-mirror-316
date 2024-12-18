# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import datetime as dt
from .workflow_event_error import WorkflowEventError
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class RejectedExecuteWorkflowWorkflowResultEvent(UniversalBaseModel):
    """
    The unsuccessful response from the Workflow execution containing an error specifying what went wrong.
    """

    id: str
    state: typing.Literal["REJECTED"] = "REJECTED"
    ts: dt.datetime
    error: WorkflowEventError

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
