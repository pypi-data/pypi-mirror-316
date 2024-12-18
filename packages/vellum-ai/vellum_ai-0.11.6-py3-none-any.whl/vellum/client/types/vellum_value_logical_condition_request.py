# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value_request import ArrayVellumValueRequest
import typing
from .vellum_value_request import VellumValueRequest
from .logical_operator import LogicalOperator
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ..core.pydantic_utilities import update_forward_refs


class VellumValueLogicalConditionRequest(UniversalBaseModel):
    """
    A basic condition comparing two Vellum values.
    """

    type: typing.Literal["LOGICAL_CONDITION"] = "LOGICAL_CONDITION"
    lhs_variable: VellumValueRequest
    operator: LogicalOperator
    rhs_variable: VellumValueRequest

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValueRequest, VellumValueLogicalConditionRequest=VellumValueLogicalConditionRequest)
