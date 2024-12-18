# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .test_suite_run_workflow_release_tag_exec_config_data import TestSuiteRunWorkflowReleaseTagExecConfigData
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class TestSuiteRunWorkflowReleaseTagExecConfig(UniversalBaseModel):
    """
    Execution configuration for running a Test Suite against a Workflow Deployment
    """

    type: typing.Literal["WORKFLOW_RELEASE_TAG"] = "WORKFLOW_RELEASE_TAG"
    data: TestSuiteRunWorkflowReleaseTagExecConfigData
    test_case_ids: typing.Optional[typing.List[str]] = pydantic.Field(default=None)
    """
    Optionally specify a subset of test case ids to run. If not provided, all test cases within the test suite will be run by default.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
