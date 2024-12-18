import pytest

from vellum.workflows.errors.types import VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.core.retry_node.node import RetryNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.state.base import BaseState, StateMeta


def test_retry_node__retry_on_error_code__successfully_retried():
    # GIVEN a retry node that is configured to retry on PROVIDER_ERROR
    @RetryNode.wrap(max_attempts=3, retry_on_error_code=VellumErrorCode.PROVIDER_ERROR)
    class TestNode(BaseNode):
        attempt_number = RetryNode.SubworkflowInputs.attempt_number

        class Outputs(BaseOutputs):
            execution_count: int

        def run(self) -> Outputs:
            if self.attempt_number < 3:
                raise NodeException(message="This will be retried", code=VellumErrorCode.PROVIDER_ERROR)

            return self.Outputs(execution_count=self.attempt_number)

    # WHEN the node is run and throws a PROVIDER_ERROR
    node = TestNode(state=BaseState())
    outputs = node.run()

    # THEN the exception is retried
    assert outputs.execution_count == 3


def test_retry_node__retry_on_error_code__missed():
    # GIVEN a retry node that is configured to retry on PROVIDER_ERROR
    @RetryNode.wrap(max_attempts=3, retry_on_error_code=VellumErrorCode.PROVIDER_ERROR)
    class TestNode(BaseNode):
        attempt_number = RetryNode.SubworkflowInputs.attempt_number

        class Outputs(BaseOutputs):
            execution_count: int

        def run(self) -> Outputs:
            if self.attempt_number < 3:
                raise Exception("This will not be retried")

            return self.Outputs(execution_count=self.attempt_number)

    # WHEN the node is run and throws a different exception
    node = TestNode(state=BaseState())
    with pytest.raises(NodeException) as exc_info:
        node.run()

    # THEN the exception is not retried
    assert (
        exc_info.value.message
        == "Unexpected rejection on attempt 1: INTERNAL_ERROR.\nMessage: This will not be retried"
    )
    assert exc_info.value.code == VellumErrorCode.INVALID_OUTPUTS


def test_retry_node__use_parent_inputs_and_state():
    # GIVEN a parent workflow Inputs and State
    class Inputs(BaseInputs):
        foo: str

    class State(BaseState):
        bar: str

    # AND a retry node that uses the parent's inputs and state
    @RetryNode.wrap(max_attempts=3, retry_on_error_code=VellumErrorCode.PROVIDER_ERROR)
    class TestNode(BaseNode):
        foo = Inputs.foo
        bar = State.bar

        class Outputs(BaseOutputs):
            value: str

        def run(self) -> Outputs:
            return self.Outputs(value=f"{self.foo} {self.bar}")

    # WHEN the node is run
    node = TestNode(
        state=State(
            bar="bar",
            meta=StateMeta(workflow_inputs=Inputs(foo="foo")),
        )
    )
    outputs = node.run()

    # THEN the data is used successfully
    assert outputs.value == "foo bar"
