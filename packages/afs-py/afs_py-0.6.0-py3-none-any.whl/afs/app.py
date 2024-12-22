import contextlib
import importlib
import inspect
import re
import textwrap
import typing

import fastapi
import pydantic
import pydantic_settings
from loguru import logger
from openai.types.beta.function_tool import FunctionTool
from openai.types.beta.threads.required_action_function_tool_call import (
    Function,
    RequiredActionFunctionToolCall,
)
from openai.types.beta.threads.run import RequiredActionSubmitToolOutputs
from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from openai.types.shared.function_definition import FunctionDefinition

import afs
from afs.types.pagination import Pagination
from afs.types.tool_output import ToolOutput

type AfsFunctions = typing.Dict[typing.Text, typing.Type[afs.AfsBaseModel]]


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> typing.AsyncIterator[None]:
    """
    Manages the application lifecycle, setting up and tearing down resources.

    Handles initialization of application settings, database connections, and AFS functions.
    Validates and loads function configurations during startup, managing duplicate function
    names and configuration validation.

    Notes
    -----
    - Initializes MongoDB connection using environment settings
    - Loads and validates AFS functions from configured modules
    - Handles duplicate function names with warning messages
    - Uses contextlib to ensure proper resource cleanup
    """  # noqa: E501

    import pymongo

    # Setup application
    logger.debug("Setting up application")
    app_settings = AppSettings()
    app.state.settings = app_settings
    app.state.logger = logger
    app.state.db = pymongo.MongoClient(
        app_settings.AFS_DATABASE_CONNECTION_STRING.get_secret_value(),
    )

    # Load AFS functions
    logger.debug("Loading AFS functions")
    afs_functions: typing.Dict[typing.Text, typing.Type[afs.AfsBaseModel]] = {}
    for module_name in app_settings.AFS_FUNCTIONS:
        logger.debug(f"Reading module: '{module_name}'")
        _mod = importlib.import_module(module_name)

        for cls_name, _cls in inspect.getmembers(_mod, inspect.isclass):
            if (
                _cls.__module__ == _mod.__name__  # The class is defined in the module
                and issubclass(
                    _cls, afs.AfsBaseModel
                )  # The class is a subclass of AfsBaseModel
            ):  # Filter out non-AFS classes
                logger.debug(f"Validating AFS class: '{cls_name}'")

                # Validate the function config
                _cls.afs_config.raise_if_invalid()

                _func_name = _cls.afs_config.name

                # Check for duplicate function names
                if _func_name in afs_functions:
                    logger.warning(
                        "There are multiple functions with the same name: "
                        + f"{_func_name}, overwriting the first one."
                        + "You might want to rename one of them to "
                        + "avoid this issue."
                    )

                afs_functions[_func_name] = _cls
                logger.info(f"Added function: '{_func_name}'")

    app.state.afs_functions = afs_functions

    yield


def create_app() -> fastapi.FastAPI:
    """
    Creates and configures the FastAPI application instance.

    Initializes a FastAPI application with OpenAI function tools integration, setting up
    routes for function management and execution. Configures application metadata,
    documentation, and dependency injection for AFS functions.

    Notes
    -----
    - Sets up API documentation with detailed descriptions
    - Configures routes for function listing, retrieval, and execution
    - Integrates with OpenAI's function calling capabilities
    - Provides standardized endpoints for both chat and assistant interactions
    """

    logger.debug("Creating application")
    app = fastapi.FastAPI(
        title="AFS API",
        summary="API service for executing OpenAI function tools with ease",
        description=textwrap.dedent(
            """
            AFS API provides endpoints to manage and execute OpenAI function tools in a standardized way.

            Key features:
            - List and retrieve available function definitions
            - Execute functions via direct invocation
            - Handle OpenAI Chat Completion tool calls
            - Support for OpenAI Assistant tool calls
            - Built-in support for weather forecasts and geocoding functions

            The API integrates with OpenAI's function calling capabilities and provides a consistent interface
            for executing functions across different services like Azure Maps and Google Maps.
            """  # noqa: E501
        ).strip(),
        version=afs.__version__,
        lifespan=lifespan,
    )

    def depends_afs_functions(request: fastapi.Request) -> AfsFunctions:
        return app.state.afs_functions

    # Add routes
    @app.get(
        "/functions",
        summary="List Available Functions",
        description="Retrieves a paginated list of all available function definitions that can be used as OpenAI function tools. Each function includes its name, description, and parameter schema.",  # noqa: E501
    )
    async def api_list_functions(
        request: fastapi.Request,
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> Pagination[FunctionDefinition]:
        """
        Lists all available function definitions in a paginated format.

        Retrieves registered AFS functions and returns their definitions in a standardized
        format compatible with OpenAI function tools. Includes function names, descriptions,
        and parameter schemas.
        """  # noqa: E501

        return Pagination(
            data=[m.function_definition for m in list(afs_functions.values())]
        )

    @app.get(
        "/functions/{function_name}",
        summary="Retrieve Function Definition",
        description="Retrieves the complete function definition for a specific function by its name. Returns detailed information including the function's name, description, parameters schema, and required fields.",  # noqa: E501
    )
    async def api_retrieve_function(
        request: fastapi.Request,
        function_name: typing.Text = fastapi.Path(...),
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> FunctionDefinition:
        """
        Retrieves detailed information about a specific function.

        Returns complete function definition including name, description, parameters schema,
        and required fields. Raises 404 error if function is not found.
        """  # noqa: E501

        if function_name not in afs_functions:
            raise fastapi.HTTPException(status_code=404, detail="Function not found")

        afs_model = afs_functions[function_name]
        return afs_model.function_definition

    @app.get(
        "/function_tools",
        summary="List Available Function Tools",
        description="Retrieves a paginated list of all available function tools that can be used as OpenAI function tools. Each function tool includes its name, description, and parameter schema.",  # noqa: E501
    )
    async def api_list_function_tools(
        request: fastapi.Request,
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> Pagination[FunctionTool]:
        """
        Retrieve a paginated list of all available OpenAI function tools.

        Returns a standardized list of function tools compatible with OpenAI's function
        calling interface. Each tool includes complete metadata and schema information
        required for integration with OpenAI's API.

        Notes
        -----
        - Returns tools in OpenAI's FunctionTool format
        - Includes parameter schemas and validation rules
        - Supports pagination for large sets of tools
        - Tools are derived from registered AFS function models
        """  # noqa: E501

        return Pagination(data=[m.function_tool for m in list(afs_functions.values())])

    @app.get(
        "/function_tools/{function_name}",
        summary="Retrieve Function Tool",
        description="Retrieves the complete function tool for a specific function by its name. Returns detailed information including the function's name, description, parameters schema, and required fields.",  # noqa: E501
    )
    async def api_retrieve_function_tool(
        request: fastapi.Request,
        function_name: typing.Text = fastapi.Path(...),
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> FunctionTool:
        """
        Retrieve detailed information about a specific OpenAI function tool.

        Fetches complete function tool definition by name, including all metadata
        required for OpenAI function calling integration. Validates function
        existence and returns standardized tool format.

        Notes
        -----
        - Returns OpenAI FunctionTool format
        - Includes complete parameter schemas
        - Raises 404 if function not found
        - Supports direct integration with OpenAI API
        """

        if function_name not in afs_functions:
            raise fastapi.HTTPException(status_code=404, detail="Function not found")

        return afs_functions[function_name].function_tool

    @app.post(
        "/functions/invoke",
        summary="Invoke Function",
        description="Executes a specific function with the provided arguments. The function must be registered in the system. Returns the function's execution result in a standardized format.",  # noqa: E501
    )
    async def api_invoke_function(
        function_invoke_request: Function = fastapi.Body(...),
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> FunctionInvokeResponse:
        """
        Executes a specified function with provided arguments.

        Validates function existence and arguments, executes the function, and returns
        results in a standardized format. Handles parameter validation and error cases.
        """

        if function_invoke_request.name not in afs_functions:
            raise fastapi.HTTPException(status_code=404, detail="Function not found")

        afs_model = afs_functions[function_invoke_request.name]
        afs_obj = afs_model.from_args_str(function_invoke_request.arguments)
        await afs_obj.execute()
        return FunctionInvokeResponse(result=afs_obj.content_parsed)

    @app.post(
        "/chat/tool_call",
        summary="Handle Chat-Based Tool Calls",
        description="Processes tool call requests initiated via chat interfaces. This endpoint validates the requested function, executes it with the provided arguments, and returns the result formatted for chat interactions.",  # noqa: E501
    )
    async def api_chat_tool_call(
        request: fastapi.Request,
        chat_completion_message_tool_call: ChatCompletionMessageToolCall,
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> ChatCompletionToolMessageParam:
        """
        Processes tool calls initiated through chat interfaces.

        Handles OpenAI chat completion tool calls, executing requested functions and
        formatting responses for chat interactions. Maintains tool call context and IDs.
        """

        if chat_completion_message_tool_call.function.name not in afs_functions:
            raise fastapi.HTTPException(status_code=404, detail="Function not found")

        # Create the AFS model
        afs_model = afs_functions[chat_completion_message_tool_call.function.name]
        afs_obj = afs_model.from_args_str(
            chat_completion_message_tool_call.function.arguments
        )
        afs_obj.set_tool_call_id(chat_completion_message_tool_call.id)

        # Execute the function
        await afs_obj.execute()

        # Return the tool message
        return ChatCompletionToolMessageParam(
            {
                "role": "tool",
                "content": afs_obj.content_parsed,
                "tool_call_id": chat_completion_message_tool_call.id,
            }
        )

    @app.post(
        "/assistant/tool_call",
        summary="Execute Assistant-Initiated Tool Call",
        description="Handles tool call requests initiated by assistant actions. This endpoint ensures the requested function exists, executes it with the provided arguments, and returns the tool's output.",  # noqa: E501
    )
    async def api_assistant_tool_call(
        request: fastapi.Request,
        required_action_function_tool_call: RequiredActionFunctionToolCall,
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> ToolOutput:
        """
        Executes tool calls initiated by OpenAI assistants.

        Processes single function execution requests from assistants, handling validation,
        execution, and response formatting. Maintains assistant context and tool call IDs.
        """  # noqa: E501

        if required_action_function_tool_call.function.name not in afs_functions:
            raise fastapi.HTTPException(status_code=404, detail="Function not found")

        # Create the AFS model
        afs_model = afs_functions[required_action_function_tool_call.function.name]
        afs_obj = afs_model.from_args_str(
            required_action_function_tool_call.function.arguments
        )
        afs_obj.set_tool_call_id(required_action_function_tool_call.id)

        # Execute the function
        await afs_obj.execute()

        # Return the tool output
        return afs_obj.tool_output

    @app.post(
        "/assistant/tool_calls",
        summary="Batch Execute Multiple Assistant-Initiated Tool Calls",
        description="Processes a batch of tool call requests initiated by assistant actions. This endpoint validates each requested function, executes them concurrently with the provided arguments, and returns a consolidated response containing all tool outputs.",  # noqa: E501
    )
    async def api_assistant_tool_calls(
        request: fastapi.Request,
        required_action_submit_tool_outputs: RequiredActionSubmitToolOutputs,
        afs_functions: AfsFunctions = fastapi.Depends(depends_afs_functions),
    ) -> AssistantToolCallsResponse:
        """
        Processes batch execution of multiple assistant tool calls.

        Handles multiple function executions in sequence, validating each function and
        consolidating results. Returns combined tool outputs for assistant processing.
        """

        for tool_call in required_action_submit_tool_outputs.tool_calls:
            if tool_call.function.name not in afs_functions:
                raise fastapi.HTTPException(
                    status_code=404,
                    detail=f"Function '{tool_call.function.name}' not found",
                )

        # Execute the functions
        tool_outputs: typing.List[ToolOutput] = []
        for tool_call in required_action_submit_tool_outputs.tool_calls:
            afs_model = afs_functions[tool_call.function.name]
            afs_obj = afs_model.from_args_str(tool_call.function.arguments)
            afs_obj.set_tool_call_id(tool_call.id)

            await afs_obj.execute()

            tool_outputs.append(afs_obj.tool_output)

        return AssistantToolCallsResponse(tool_outputs=tool_outputs)

    return app


class AppSettings(pydantic_settings.BaseSettings):
    """
    Application configuration settings using Pydantic.

    Manages environment-based configuration for database connections, function
    repositories, and AFS function loading. Includes validation and parsing of
    configuration values.

    Notes
    -----
    - Handles database connection strings with secure secret management
    - Provides configuration for function repository management
    - Supports comma-separated function module lists
    """

    AFS_DATABASE_CONNECTION_STRING: pydantic.SecretStr = pydantic.Field(
        default=pydantic.SecretStr("mongodb://localhost:27017/"),
        description="The connection string to the AFS database",
    )
    AFS_DATABASE_NAME: str = pydantic.Field(
        default="afs",
        description="The name of the AFS database",
    )
    AFS_FUNCTIONS_REPOSITORY_TABLE_NAME: str = pydantic.Field(
        default="functions",
        description="The name of the AFS functions repository table",
    )
    AFS_FUNCTIONS: typing.List[typing.Text] = pydantic.Field(
        default_factory=lambda: [
            "afs.functions.azure.get_weather_forecast_daily",
            "afs.functions.azure.get_weather_forecast_hourly",
            "afs.functions.google.get_maps_geocode",
            "afs.functions.assorted.currencies",
        ],
        description="The list of AFS functions",
    )

    @pydantic.field_validator("AFS_FUNCTIONS", mode="before")
    def split_afs_functions(cls, value):
        """
        Parse and split AFS function paths from string or list input.

        Processes function module paths provided either as a comma/semicolon-separated
        string or as a list. Handles string cleaning and validation to ensure proper
        module path formatting.

        Notes
        -----
        - Supports both string and list inputs
        - Handles comma and semicolon separators
        - Strips whitespace and quotes from paths
        - Filters out empty strings

        Examples
        --------
        >>> split_afs_functions("module1.func1, module2.func2")
        ['module1.func1', 'module2.func2']
        >>> split_afs_functions("'module1.func1';'module2.func2'")
        ['module1.func1', 'module2.func2']
        """

        if isinstance(value, typing.Text):
            output: typing.List[typing.Text] = []
            for s in re.split(r"[;,]", value):
                s = s.strip(" '\"").strip()
                if s:
                    output.append(s)
            return output
        return value


class FunctionInvokeResponse(pydantic.BaseModel):
    result: typing.Any


class AssistantToolCallsResponse(pydantic.BaseModel):
    tool_outputs: typing.List[ToolOutput]


app = create_app()
