import inspect
from typing import Any, ClassVar, Dict, Generic, List, Optional, Sequence, Tuple, Type, TypeVar, cast, get_args

from vellum import (
    ArrayInput,
    ChatHistoryInput,
    ChatMessage,
    CodeExecutionPackage,
    CodeExecutionRuntime,
    CodeExecutorInput,
    ErrorInput,
    FunctionCall,
    FunctionCallInput,
    JsonInput,
    NumberInput,
    SearchResult,
    SearchResultsInput,
    StringInput,
    VellumError,
    VellumValue,
)
from vellum.core import RequestOptions
from vellum.workflows.errors.types import VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.bases.base import BaseNodeMeta
from vellum.workflows.nodes.displayable.code_execution_node.utils import read_file_from_path
from vellum.workflows.outputs.base import BaseOutputs
from vellum.workflows.types.core import EntityInputsInterface, VellumSecret
from vellum.workflows.types.generics import StateType
from vellum.workflows.types.utils import get_original_base
from vellum.workflows.utils.vellum_variables import primitive_type_to_vellum_variable_type

_OutputType = TypeVar("_OutputType")


# TODO: Consolidate all dynamic output metaclasses
# https://app.shortcut.com/vellum/story/5533
class _CodeExecutionNodeMeta(BaseNodeMeta):
    def __new__(mcs, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]) -> Any:
        parent = super().__new__(mcs, name, bases, dct)

        # We use the compiled class to infer the output type for the Outputs.result descriptor.
        if not isinstance(parent, _CodeExecutionNodeMeta):
            raise ValueError("CodeExecutionNode must be created with the CodeExecutionNodeMeta metaclass")

        annotations = parent.__dict__["Outputs"].__annotations__
        parent.__dict__["Outputs"].__annotations__ = {
            **annotations,
            "result": parent.get_output_type(),
        }
        return parent

    def get_output_type(cls) -> Type:
        original_base = get_original_base(cls)
        all_args = get_args(original_base)

        if len(all_args) < 2 or isinstance(all_args[1], TypeVar):
            return str
        else:
            return all_args[1]


class CodeExecutionNode(BaseNode[StateType], Generic[StateType, _OutputType], metaclass=_CodeExecutionNodeMeta):
    """
    Used to execute an arbitrary script. This node exists to be backwards compatible with
    Vellum's Code Execution Node, and for most cases, you should extend from `BaseNode` directly.

    filepath: str - The path to the script to execute.
    code_inputs: EntityInputsInterface - The inputs for the custom script.
    runtime: CodeExecutionRuntime = "PYTHON_3_12" - The runtime to use for the custom script.
    packages: Optional[Sequence[CodeExecutionPackage]] = None - The packages to use for the custom script.
    request_options: Optional[RequestOptions] = None - The request options to use for the custom script.
    """

    filepath: ClassVar[str]

    code_inputs: ClassVar[EntityInputsInterface]
    runtime: CodeExecutionRuntime = "PYTHON_3_11_6"
    packages: Optional[Sequence[CodeExecutionPackage]] = None

    request_options: Optional[RequestOptions] = None

    class Outputs(BaseOutputs):
        # We use our mypy plugin to override the _OutputType with the actual output type
        # for downstream references to this output.
        result: _OutputType  # type: ignore[valid-type]
        log: str

    def run(self) -> Outputs:
        input_values = self._compile_code_inputs()
        expected_output_type = primitive_type_to_vellum_variable_type(self.__class__.get_output_type())
        code_execution = self._context.vellum_client.execute_code(
            input_values=input_values,
            code=self._resolve_code(),
            runtime=self.runtime,
            output_type=expected_output_type,
            packages=self.packages or [],
            request_options=self.request_options,
        )

        if code_execution.output.type != expected_output_type:
            raise NodeException(
                code=VellumErrorCode.INVALID_OUTPUTS,
                message=f"Expected an output of type '{expected_output_type}', received '{code_execution.output.type}'",
            )

        return self.Outputs(result=code_execution.output.value, log=code_execution.log)

    def _compile_code_inputs(self) -> List[CodeExecutorInput]:
        # TODO: We may want to consolidate with prompt deployment input compilation
        # https://app.shortcut.com/vellum/story/4117

        compiled_inputs: List[CodeExecutorInput] = []

        for input_name, input_value in self.code_inputs.items():
            if isinstance(input_value, str):
                compiled_inputs.append(
                    StringInput(
                        name=input_name,
                        value=str(input_value),
                    )
                )
            elif isinstance(input_value, VellumSecret):
                compiled_inputs.append(
                    # TODO: Expose a VellumSecret type from the Vellum SDK
                    # https://app.shortcut.com/vellum/story/4785
                    {  # type: ignore[arg-type]
                        "name": input_name,
                        "type": "SECRET",
                        "value": input_value.name,
                    }
                )
            elif isinstance(input_value, list):
                if all(isinstance(message, ChatMessage) for message in input_value):
                    compiled_inputs.append(
                        ChatHistoryInput(
                            name=input_name,
                            value=cast(List[ChatMessage], input_value),
                        )
                    )
                elif all(isinstance(message, SearchResult) for message in input_value):
                    compiled_inputs.append(
                        SearchResultsInput(
                            name=input_name,
                            value=cast(List[SearchResult], input_value),
                        )
                    )
                else:
                    compiled_inputs.append(
                        ArrayInput(
                            name=input_name,
                            value=cast(List[VellumValue], input_value),
                        )
                    )
            elif isinstance(input_value, dict):
                compiled_inputs.append(
                    JsonInput(
                        name=input_name,
                        value=cast(Dict[str, Any], input_value),
                    )
                )
            elif isinstance(input_value, float):
                compiled_inputs.append(
                    NumberInput(
                        name=input_name,
                        value=input_value,
                    )
                )
            elif isinstance(input_value, FunctionCall):
                compiled_inputs.append(
                    FunctionCallInput(
                        name=input_name,
                        value=cast(FunctionCall, input_value),
                    )
                )
            elif isinstance(input_value, VellumError):
                compiled_inputs.append(
                    ErrorInput(
                        name=input_name,
                        value=cast(VellumError, input_value),
                    )
                )
            else:
                raise NodeException(
                    message=f"Unrecognized input type for input '{input_name}'",
                    code=VellumErrorCode.INVALID_INPUTS,
                )

        return compiled_inputs

    def _resolve_code(self) -> str:
        root = inspect.getfile(self.__class__)
        code = read_file_from_path(node_filepath=root, script_filepath=self.filepath)
        if not code:
            raise NodeException(
                message=f"Filepath '{self.filepath}' does not exist",
                code=VellumErrorCode.INVALID_INPUTS,
            )

        return code
