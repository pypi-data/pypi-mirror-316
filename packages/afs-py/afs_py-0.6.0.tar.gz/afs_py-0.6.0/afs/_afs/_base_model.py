import json
import random
import string
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Coroutine,
    Optional,
    ParamSpec,
    Text,
    TypeVar,
)

import openai
from json_repair import repair_json
from openai.types.beta.threads import run_submit_tool_outputs_params
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from pydantic import BaseModel, PrivateAttr

from ._config import AfsConfig
from ._descriptors import AfsDescriptors
from ._parser import AfsParser

if TYPE_CHECKING:
    from afs.types.chat_completion_tool_message import ChatCompletionToolMessage
    from afs.types.tool_output import ToolOutput


R = TypeVar("R")
P = ParamSpec("P")


FunctionType = Callable[P, R]  # Regular function type
CoroutineType = Callable[P, Coroutine[Any, Any, R]]  # Coroutine function type


# tags: <override>
class _OverridesFunctionConfig(BaseModel):
    """
    Base configuration class for AFS function tools that must be overridden by user implementations.

    This class defines the core configuration structure that all AFS function tools must implement.
    It requires users to override the afs_config class variable with their specific function
    configuration details.

    Notes
    -----
    The afs_config class variable must be set to an instance of AfsConfig containing:
    - name: Function identifier
    - description: Function purpose and behavior
    - function: Import path to the callable function

    Examples
    --------
    >>> class MyFunctionConfig(AfsBaseModel):
    ...     afs_config: ClassVar[AfsConfig] = AfsConfig(
    ...         name="my_function",
    ...         description="Does something useful",
    ...         function="module.path.to.function"
    ...     )
    """  # noqa: E501

    # Must be overridden by the user to
    # define the function name, description and function path
    afs_config: ClassVar[AfsConfig]


# tags: <override>
class _OverridesFunctionArguments(BaseModel):
    """
    Base arguments class for AFS function tools that defines the function's parameter schema.

    This class serves as a template for defining function arguments in AFS tools. Users must
    extend this class to specify their function's input parameters using Pydantic field
    definitions.

    Notes
    -----
    All function parameters should be defined as class attributes using pydantic.Field
    with appropriate type hints and descriptions.

    Examples
    --------
    >>> class MyFunctionArgs(AfsBaseModel):
    ...     name: str = Field(..., description="User's name")
    ...     age: int = Field(default=0, description="User's age")
    """  # noqa: E501

    # Function arguments
    # <function_arguments>
    pass


# tags: <internal>
class _InternalFunctionRuntime(BaseModel, AfsDescriptors):
    """
    Internal runtime class that manages function execution state and content handling.

    This class provides core functionality for managing function execution state, tool call IDs,
    and response content. It includes properties and methods for accessing and manipulating
    function execution results.

    Notes
    -----
    - Content must be set via execute() or sync_execute() before accessing
    - Tool call IDs are used for OpenAI function calling integration
    - Content can be accessed through various properties that format the response
    appropriately for different use cases (raw content, tool messages, etc.)

    Examples
    --------
    >>> instance = MyFunction()
    >>> await instance.execute()
    >>> content = instance.content  # Access execution results
    >>> tool_msg = instance.tool_message  # Get formatted tool message
    """  # noqa: E501

    # Private attributes
    _tool_call_id: Optional[Text] = PrivateAttr(default=None)
    _content: Optional[Any | openai.NotGiven] = PrivateAttr(default=openai.NOT_GIVEN)

    @property
    def content(self) -> Any:
        """
        Get the function execution result content.

        Raises
        ------
        ValueError
            If content is not set (function not executed yet)
        """

        if self._content is openai.NOT_GIVEN:
            raise ValueError(
                "Response content is not set, please execute the function first."
            )
        return self._content

    @property
    def is_content_null(self) -> bool:
        """
        Check if the content is None.

        Used to determine if the function execution resulted in null content,
        which may indicate execution failure or empty results.
        """

        return self._content is None

    def set_tool_call_id(self, tool_call_id: Text) -> None:
        """
        Set the OpenAI tool call identifier.

        Used for tracking and associating function calls with OpenAI's function
        calling system. This ID is essential for proper message threading and
        response mapping.
        """

        self._tool_call_id = tool_call_id

    def set_content(self, content: Any) -> None:
        """
        Set the function execution result content.

        This method is typically called after function execution to store
        the result for later access through various formatting properties.
        """

        self._content = content


class AfsBaseModel(
    _OverridesFunctionConfig,
    _OverridesFunctionArguments,
    _InternalFunctionRuntime,
    AfsParser,
):
    """
    A base model class for creating OpenAI function tool-compatible implementations.

    This class serves as the foundation for defining custom functions that can be used
    with OpenAI's function calling features. It combines configuration, argument handling,
    and runtime execution capabilities through multiple inheritance.

    Notes
    -----
    The class requires implementation of two key components:
    - Function configuration via afs_config class variable
    - Function arguments schema through Pydantic field definitions

    The class provides built-in support for:
    - OpenAI function tool integration
    - Async and sync execution modes
    - Content parsing and formatting
    - Tool message generation for chat completions
    - Tool output handling for assistant API

    Examples
    --------
    >>> class MyFunction(AfsBaseModel):
    ...     # Define function configuration
    ...     afs_config: ClassVar[AfsConfig] = AfsConfig(
    ...         name="my_function",
    ...         description="Does something useful",
    ...         function="module.path.to.function"
    ...     )
    ...
    ...     # Define function arguments
    ...     input_text: str = Field(..., description="Input text to process")
    ...
    ...     @classmethod
    ...     def parse_content(cls, response: Any) -> str:
    ...         return str(response).upper()

    >>> # Execute the function
    >>> func = MyFunction(input_text="hello")
    >>> await func.execute()
    >>> result = func.content_parsed
    """  # noqa: E501

    @classmethod
    def from_args_str(cls, args_str: Optional[Text]):
        """
        Create an instance from a JSON string containing function arguments.

        Parses a JSON string containing function arguments and creates a new instance
        of the model. Uses json_repair to handle potentially malformed JSON input.

        Notes
        -----
        - If args_str is None or empty, creates instance with empty dict
        - Repairs malformed JSON using json_repair library
        - Validates arguments against model schema

        Examples
        --------
        >>> args = '{"name": "test", "value": 123}'
        >>> instance = MyModel.from_args_str(args)
        """  # noqa: E501

        func_kwargs = (
            json.loads(repair_json(args_str)) if args_str else {}  # type: ignore
        )
        return cls.model_validate(func_kwargs)

    @classmethod
    def is_base_model_valid(cls, config: Optional[AfsConfig] = None) -> bool:
        """
        Validate the model's configuration.

        Checks if the provided or default configuration meets validity requirements.
        Configuration can be provided explicitly or retrieved from class attributes.

        Notes
        -----
        - Checks config validity using AfsConfig.is_valid()
        - Falls back to class afs_config if no config provided
        - Raises ValueError if no valid configuration found

        Examples
        --------
        >>> config = AfsConfig(name="test", description="Test function", function="module.func")
        >>> MyModel.is_base_model_valid(config)
        True
        """  # noqa: E501

        if config is not None:
            return config.is_valid()
        if hasattr(cls, "afs_config"):
            return cls.afs_config.is_valid()
        else:
            raise ValueError(
                "No configuration provided and no default configuration found."
            )

    @property
    def content_parsed(self) -> Any:
        """
        Get the parsed version of the function execution content.

        Returns the function response content after processing through the model's
        parse_content() method, which can be customized by subclasses for specific
        formatting needs.

        Notes
        -----
        - Requires content to be set via execute() or sync_execute() first
        - Uses the model's parse_content() method for formatting
        - Raises ValueError if content not set
        """

        return self.parse_content(self.content)

    @property
    def tool_message(self) -> "ChatCompletionToolMessage":
        """
        Get the function result formatted as an OpenAI chat completion tool message.

        Creates a structured message containing the parsed content and tool call ID
        suitable for use in chat completions. Generates a random tool call ID if
        none was provided.

        Notes
        -----
        - Requires content to be set via execute() or sync_execute()
        - Automatically generates tool_call_id if not set
        - Returns ChatCompletionToolMessage with content and ID
        """

        from afs.config import logger

        tool_call_id = self._tool_call_id
        if tool_call_id is None:
            logger.warning(
                "No tool call id found, you might want to set the tool call id "
                + "provided by the LLM API.",
            )
            tool_call_id = "tool_" + "".join(
                random.choices(string.ascii_letters + string.digits, k=12)
            )
        return self.parse_content_as_openai_tool_message(
            self.content, tool_call_id=tool_call_id
        )

    @property
    def tool_message_param(self) -> "ChatCompletionToolMessageParam":
        """
        Get the function result as a parameter-ready chat completion tool message.

        Converts the tool message into a format suitable for direct use as a parameter
        in OpenAI API calls. Excludes any None values from the output.

        Notes
        -----
        - Builds upon tool_message property
        - Excludes None values from output
        - Returns dict-like structure for API parameters
        """

        return self.tool_message.model_dump(exclude_none=True)  # type: ignore

    @property
    def tool_output(self) -> "ToolOutput":
        """
        Get the function result formatted as an OpenAI assistant tool output.

        Creates a structured output containing the parsed content and tool call ID
        suitable for use with OpenAI's assistant API. Generates a random tool call
        ID if none was provided.

        Notes
        -----
        - Requires content to be set via execute() or sync_execute()
        - Automatically generates tool_call_id if not set
        - Returns ToolOutput with content and ID
        """

        from afs.config import logger

        tool_call_id = self._tool_call_id
        if tool_call_id is None:
            logger.warning(
                "No tool call id found, you might want to set the tool call id "
                + "provided by the LLM API.",
            )
            tool_call_id = "tool_" + "".join(
                random.choices(string.ascii_letters + string.digits, k=12)
            )

        return self.parse_content_as_assistant_tool_output(
            self.content, tool_call_id=tool_call_id
        )

    @property
    def tool_output_param(self) -> "run_submit_tool_outputs_params.ToolOutput":
        """
        Get the function result as a parameter-ready assistant tool output.

        Converts the tool output into a format suitable for direct use as a parameter
        in OpenAI Assistant API calls. Excludes any None values from the output.

        Notes
        -----
        - Builds upon tool_output property
        - Excludes None values from output
        - Returns dict-like structure for API parameters
        """

        return self.tool_output.model_dump(exclude_none=True)  # type: ignore

    async def execute(self) -> Any:
        """
        Execute the configured function asynchronously.

        Retrieves and executes the function specified in afs_config, storing the result
        in the model's content attribute. Returns the function result directly while
        also making it available via the content property.

        Notes
        -----
        - Function must be properly configured in afs_config
        - Result accessible via content property after execution
        - Handles both regular and coroutine functions

        Examples
        --------
        >>> instance = MyFunction(input="test")
        >>> result = await instance.execute()
        >>> assert result == instance.content
        """  # noqa: E501

        from afs.utils.run import run_func

        func = self.afs_config.get_function()

        func_res = await run_func(func, self)
        self.set_content(func_res)
        return func_res

    def sync_execute(self) -> Any:
        """
        Execute the configured function synchronously.

        Synchronous version of execute(). Retrieves and executes the function specified
        in afs_config, storing the result in the model's content attribute. Returns the
        function result directly while also making it available via the content property.

        Notes
        -----
        - Function must be properly configured in afs_config
        - Result accessible via content property after execution
        - Use for non-async functions or when async execution not needed

        Examples
        --------
        >>> instance = MyFunction(input="test")
        >>> result = instance.sync_execute()
        >>> assert result == instance.content
        """  # noqa: E501

        from afs.utils.run import sync_run_func

        func = self.afs_config.get_function()
        func_res = sync_run_func(func, self)
        self.set_content(func_res)
        return func_res
