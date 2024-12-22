from typing import TYPE_CHECKING, List, Sequence, Type

from openai.types.beta.function_tool import FunctionTool

if TYPE_CHECKING:
    import afs


def from_base_model(
    base_model_type: Type["afs.AfsBaseModel"] | "afs.AfsBaseModel",
) -> "FunctionTool":
    import afs.utils.function_definition

    return FunctionTool.model_validate(
        {
            "function": afs.utils.function_definition.from_base_model(base_model_type),
            "type": "function",
        }
    )


def from_base_models(
    base_model_types: Sequence[Type["afs.AfsBaseModel"] | "afs.AfsBaseModel"],
) -> List["FunctionTool"]:
    return [from_base_model(base_model_type) for base_model_type in base_model_types]
