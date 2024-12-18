# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .test_suite_test_case_replaced_bulk_result_data import TestSuiteTestCaseReplacedBulkResultData
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TestSuiteTestCaseReplacedBulkResult(UniversalBaseModel):
    """
    The result of a bulk operation that replaced a Test Case.
    """

    id: str = pydantic.Field()
    """
    An ID that maps back to one of the initially supplied operations. Can be used to determine the result of a given operation.
    """

    type: typing.Literal["REPLACED"] = "REPLACED"
    data: TestSuiteTestCaseReplacedBulkResultData

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
