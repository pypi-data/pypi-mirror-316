from unittest import mock

from deepdiff import DeepDiff

from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.workflows import VellumWorkflowDisplay
from vellum_ee.workflows.display.workflows.get_vellum_workflow_display_class import get_workflow_display

from tests.workflows.basic_try_node.workflow import SimpleTryExample


def test_serialize_workflow():
    # GIVEN a Workflow with a TryNode
    # WHEN we serialize it
    workflow_display = get_workflow_display(base_display_class=VellumWorkflowDisplay, workflow_class=SimpleTryExample)

    with mock.patch.object(BaseNodeVellumDisplay, "serialize") as mocked_serialize:
        mocked_serialize.return_value = {"type": "MOCKED"}
        serialized_workflow: dict = workflow_display.serialize()

    # THEN we should get a serialized representation of the Workflow
    assert serialized_workflow.keys() == {
        "workflow_raw_data",
        "input_variables",
        "output_variables",
    }

    # AND its input variables should be what we expect
    input_variables = serialized_workflow["input_variables"]
    assert len(input_variables) == 0

    # AND its output variables should be what we expect
    output_variables = serialized_workflow["output_variables"]
    assert len(output_variables) == 2
    assert not DeepDiff(
        [
            {
                "id": "d4a3117e-8ec3-4579-8eeb-5e4247bb086d",
                "key": "error",
                "type": "JSON",
            },
            {
                "id": "a8b99024-cd32-42f6-bb2f-827189bf3a3c",
                "key": "final_value",
                "type": "NUMBER",
            },
        ],
        output_variables,
        ignore_order=True,
    )

    # AND its raw data should be what we expect
    workflow_raw_data = serialized_workflow["workflow_raw_data"]
    assert workflow_raw_data.keys() == {"edges", "nodes", "display_data", "definition"}
    assert len(workflow_raw_data["edges"]) == 3
    assert len(workflow_raw_data["nodes"]) == 4

    # AND each node should be serialized correctly
    entrypoint_node = workflow_raw_data["nodes"][0]
    assert entrypoint_node == {
        "id": "c238508d-85ab-4644-8cbb-88eae457fe12",
        "type": "ENTRYPOINT",
        "inputs": [],
        "definition": {
            "bases": [],
            "module": [
                "vellum",
                "workflows",
                "nodes",
                "bases",
                "base",
            ],
            "name": "BaseNode",
        },
        "data": {
            "label": "Entrypoint Node",
            "source_handle_id": "04da0bb6-5b42-4dd1-a4e4-08f3ab03e1a3",
        },
        "display_data": {
            "position": {"x": 0.0, "y": 0.0},
        },
    }

    try_node = workflow_raw_data["nodes"][1]
    assert try_node == {"type": "MOCKED"}
