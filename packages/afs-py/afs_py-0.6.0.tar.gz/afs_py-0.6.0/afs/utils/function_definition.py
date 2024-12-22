from typing import TYPE_CHECKING, Type

from openai.types.shared.function_definition import FunctionDefinition

if TYPE_CHECKING:
    import afs


def from_base_model(
    base_model_type: Type["afs.AfsBaseModel"] | "afs.AfsBaseModel",
) -> "FunctionDefinition":
    """
    Convert an AFS base model into an OpenAI function definition.

    This function creates a standardized OpenAI function definition from an AFS base model,
    enabling seamless integration with OpenAI's function calling features. The function
    validates the base model, extracts its JSON schema, and formats it according to
    OpenAI's function definition requirements.

    Notes
    -----
    - Removes the 'title' field from the model's JSON schema to maintain clean output
    - Validates the base model before conversion using `is_base_model_valid()`
    - Uses the model's afs_config for name and description metadata

    Examples
    --------
    >>> class MyFunction(AfsBaseModel):
    ...     afs_config = AfsConfig(
    ...         name="my_function",
    ...         description="A sample function"
    ...     )
    ...     input_text: str = Field(description="Input text")
    >>> function_def = from_base_model(MyFunction)

    See Also
    --------
    afs.utils.function_tool.from_base_model : Similar conversion for function tools
    """  # noqa: E501

    if not base_model_type.is_base_model_valid():
        raise ValueError(f"The base model is invalid: {base_model_type}")

    model_json_schema = base_model_type.model_json_schema()
    model_json_schema.pop("title", None)
    return FunctionDefinition.model_validate(
        {
            "name": base_model_type.afs_config.name,
            "description": base_model_type.afs_config.description,
            "parameters": model_json_schema,
        }
    )
