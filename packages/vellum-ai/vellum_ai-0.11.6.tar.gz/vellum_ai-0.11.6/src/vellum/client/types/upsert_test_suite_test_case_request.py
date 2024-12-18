# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value_request import ArrayVellumValueRequest
import typing
import pydantic
from .named_test_case_variable_value_request import NamedTestCaseVariableValueRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..core.pydantic_utilities import update_forward_refs


class UpsertTestSuiteTestCaseRequest(UniversalBaseModel):
    id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The Vellum-generated ID of an existing Test Case whose data you'd like to replace. If specified and no Test Case exists with this ID, a 404 will be returned.
    """

    external_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    An ID external to Vellum that uniquely identifies the Test Case that you'd like to create/update. If there's a match on a Test Case that was previously created with the same external_id, it will be updated. Otherwise, a new Test Case will be created with this value as its external_id. If no external_id is specified, then a new Test Case will always be created.
    """

    label: typing.Optional[str] = pydantic.Field(default=None)
    """
    A human-readable label used to convey the intention of this Test Case
    """

    input_values: typing.List[NamedTestCaseVariableValueRequest] = pydantic.Field()
    """
    Values for each of the Test Case's input variables
    """

    evaluation_values: typing.List[NamedTestCaseVariableValueRequest] = pydantic.Field()
    """
    Values for each of the Test Case's evaluation variables
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValueRequest, UpsertTestSuiteTestCaseRequest=UpsertTestSuiteTestCaseRequest)
