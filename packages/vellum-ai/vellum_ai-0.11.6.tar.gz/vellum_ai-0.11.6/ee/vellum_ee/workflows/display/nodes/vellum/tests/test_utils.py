import pytest
from uuid import UUID, uuid4
from typing import List, cast

from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.references import OutputReference, WorkflowInputReference
from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.nodes.types import NodeOutputDisplay
from vellum_ee.workflows.display.nodes.vellum.utils import create_node_input_value_pointer_rules
from vellum_ee.workflows.display.types import WorkflowDisplayContext
from vellum_ee.workflows.display.vellum import (
    ConstantValuePointer,
    InputVariableData,
    InputVariablePointer,
    NodeDisplayData,
    NodeInputValuePointerRule,
    NodeOutputData,
    NodeOutputPointer,
    StringVellumValue,
    WorkflowInputsVellumDisplayOverrides,
    WorkflowMetaVellumDisplay,
)
from vellum_ee.workflows.display.workflows.vellum_workflow_display import VellumWorkflowDisplay


class Inputs(BaseInputs):
    example_workflow_input: str


class MyNodeA(BaseNode):
    example_node_input = Inputs.example_workflow_input

    class Outputs(BaseOutputs):
        output: str


class MyNodeB(BaseNode):
    example = MyNodeA.Outputs.output
    fallback_example = MyNodeA.Outputs.output.coalesce(Inputs.example_workflow_input).coalesce("fallback")


@pytest.mark.parametrize(
    ["descriptor", "expected_rules"],
    [
        (
            MyNodeB.example,
            [
                NodeOutputPointer(
                    data=NodeOutputData(
                        node_id="b48fa5e0-d7d3-4fe3-ae48-615415011cc5",
                        output_id="4b16a629-11a1-4b3f-a965-a57b872d13b8",
                    )
                )
            ],
        ),
        (
            MyNodeB.fallback_example,
            [
                NodeOutputPointer(
                    type="NODE_OUTPUT",
                    data=NodeOutputData(
                        node_id="b48fa5e0-d7d3-4fe3-ae48-615415011cc5",
                        output_id="4b16a629-11a1-4b3f-a965-a57b872d13b8",
                    ),
                ),
                InputVariablePointer(
                    type="INPUT_VARIABLE",
                    data=InputVariableData(input_variable_id="a154c29d-fac0-4cd0-ba88-bc52034f5470"),
                ),
                ConstantValuePointer(type="CONSTANT_VALUE", data=StringVellumValue(type="STRING", value="fallback")),
            ],
        ),
    ],
)
def test_create_node_input_value_pointer_rules(
    descriptor: BaseDescriptor, expected_rules: List[NodeInputValuePointerRule]
) -> None:
    rules = create_node_input_value_pointer_rules(
        descriptor,
        WorkflowDisplayContext(
            workflow_display_class=VellumWorkflowDisplay,
            workflow_display=WorkflowMetaVellumDisplay(
                entrypoint_node_id=uuid4(),
                entrypoint_node_source_handle_id=uuid4(),
                entrypoint_node_display=NodeDisplayData(),
            ),
            workflow_input_displays={
                cast(WorkflowInputReference, Inputs.example_workflow_input): WorkflowInputsVellumDisplayOverrides(
                    id=UUID("a154c29d-fac0-4cd0-ba88-bc52034f5470"),
                ),
            },
            node_output_displays={
                cast(OutputReference, MyNodeA.Outputs.output): (
                    MyNodeA,
                    NodeOutputDisplay(id=UUID("4b16a629-11a1-4b3f-a965-a57b872d13b8"), name="output"),
                ),
            },
            node_displays={
                MyNodeA: BaseNodeVellumDisplay(MyNodeA),
            },
        ),
    )
    assert rules == expected_rules
