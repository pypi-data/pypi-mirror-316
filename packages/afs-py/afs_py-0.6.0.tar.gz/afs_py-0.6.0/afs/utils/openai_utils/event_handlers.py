import concurrent.futures
import textwrap
import typing

import openai
from openai import AssistantEventHandler
from openai.types.beta.assistant_stream_event import AssistantStreamEvent
from openai.types.beta.threads import Message
from openai.types.beta.threads.required_action_function_tool_call import (
    RequiredActionFunctionToolCall,
)
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from typing_extensions import override

from afs import AfsBaseModel
from afs.config import logger
from afs.types.simple_message import SimpleMessage


def run_func_tool_call(
    tool_call: RequiredActionFunctionToolCall,
    *,
    records: typing.Optional[typing.List[SimpleMessage]] = None,
    tools_set: typing.Optional[typing.Iterable[typing.Type[AfsBaseModel]]] = None,
) -> "ToolOutput":
    """
    Execute a function tool call and handle its response with proper logging and error management.

    This function serves as the core executor for OpenAI function tools, managing the entire
    lifecycle of a tool call including argument parsing, execution, error handling, and
    response formatting. It maintains a record of tool executions and their outcomes.

    Notes
    -----
    - Creates a tool record entry for tracking the execution
    - Handles tool lookup failures gracefully with appropriate error messages
    - Manages argument parsing errors and execution failures
    - Truncates long output messages to 300 characters for logging
    - Thread-safe execution through the AFS model's sync_execute method

    Examples
    --------
    >>> tool_call = RequiredActionFunctionToolCall(...)
    >>> tool_output = run_func_tool_call(
    ...     tool_call,
    ...     tools_set=[MyCustomTool],
    ...     records=[]
    ... )
    >>> print(tool_output.output)
    'Function execution result'

    See Also
    --------
    AfsEventHandler : Manages the event handling for assistant interactions
    AfsBaseModel : Base class for implementing function tools
    """  # noqa: E501

    logger.info(
        f"Calling function: '{tool_call.function.name}' "
        + f"with args: '{tool_call.function.arguments}'"
    )

    records = records or []
    tools_set = list(tools_set or [])

    # Tool record
    tool_record = SimpleMessage(
        id=tool_call.id,
        role="tool",
        content=textwrap.dedent(
            f"""
            Function Name: '{tool_call.function.name}'
            Function Arguments: {tool_call.function.arguments}
            """
        ).strip(),
    )
    records.append(tool_record)

    # Pick the tool
    afs_base_model: typing.Optional[typing.Type[AfsBaseModel]] = None
    for _afs_tool in tools_set:
        if tool_call.function.name != _afs_tool.afs_config.name:
            continue
        afs_base_model = _afs_tool
        break

    # Handle the case where the function tool is not found
    if afs_base_model is None:
        logger.error(
            f"Function name '{tool_call.function.name}' not found, "
            + "available functions: "
            + f"{', '.join([t.afs_config.name for t in tools_set])}"
        )
        _tool_output_content = f"Function tool '{tool_call.function.name}' not found!"
        tool_record.set_completed_content(f"\nTool output: {_tool_output_content}")
        return ToolOutput(
            output=_tool_output_content,
            tool_call_id=tool_call.id,
        )

    # Create the AFS model
    try:
        afs_model = afs_base_model.from_args_str(tool_call.function.arguments)
        afs_model.set_tool_call_id(tool_call.id)
    except Exception as e:
        logger.exception(e)
        logger.error(f"Error creating AFS model for '{tool_call.function.name}': {e}")
        _tool_output_content = (
            f"Failed to parse arguments for function tool '{tool_call.function.name}'!"
        )
        tool_record.set_completed_content(f"\nTool output: {_tool_output_content}")
        return ToolOutput(
            output=_tool_output_content,
            tool_call_id=tool_call.id,
        )

    # Execute the function
    try:
        afs_model.sync_execute()
    except Exception as e:
        logger.exception(e)
        logger.error(f"Error executing function '{tool_call.function.name}': {e}")
        if afs_model.is_content_null:
            afs_model.set_content(afs_base_model.afs_config.error_content)

    # Add the tool output to the list
    tool_output = afs_model.tool_output_param
    _debug_out = tool_output.get("output") or ""
    _debug_out = f"{_debug_out[:300]}..." if len(_debug_out) > 300 else _debug_out
    logger.info(f"Tool output: {dict(output=_debug_out, tool_call_id=tool_call.id)}")
    tool_record.set_completed_content(f"\nTool output: {_debug_out}")

    # Return the tool output
    return tool_output


class AfsEventHandler(AssistantEventHandler):
    """
    Event handler for managing OpenAI Assistant API interactions and tool executions.

    A specialized event handler that extends OpenAI's AssistantEventHandler to manage
    function tool calls, message tracking, and event processing for the AFS (Aiello-Functions)
    framework. It provides thread-safe execution of tools and maintains a record of all
    interactions.

    Notes
    -----
    - Handles 'requires_action' events for function tool calls
    - Executes multiple tool calls concurrently using ThreadPoolExecutor
    - Maintains message history and execution records
    - Supports debug mode for detailed logging
    - Thread-safe tool execution through the AFS model's sync_execute method

    Examples
    --------
    >>> client = openai.OpenAI()
    >>> handler = AfsEventHandler(
    ...     client,
    ...     tools_set=[MyCustomTool],
    ...     messages=[],
    ...     debug=True
    ... )
    >>> with client.beta.threads.runs.stream(
    ...     thread_id=thread.id,
    ...     assistant_id=assistant.id,
    ...     tools=[tool.function_tool_param for tool in tools],
    ...     event_handler=handler,
    ... ) as stream:
    ...     stream.until_done()

    See Also
    --------
    run_func_tool_call : Core function for executing individual tool calls
    AfsBaseModel : Base class for implementing function tools
    """  # noqa: E501

    def __init__(
        self,
        client: openai.OpenAI,
        *args,
        tools_set: typing.Optional[typing.Iterable[typing.Type[AfsBaseModel]]] = None,
        messages: typing.Optional[typing.List[Message]] = None,
        records: typing.Optional[typing.List[SimpleMessage]] = None,
        debug: bool = False,
        **kwargs,
    ):
        """
        Initialize an AFS event handler for OpenAI Assistant API interactions.

        Notes
        -----
        - Initializes client connection and tool configurations
        - Sets up message tracking and record keeping
        - Configures debug mode for detailed logging
        - Inherits base functionality from OpenAI's AssistantEventHandler
        """

        super().__init__(*args, **kwargs)
        self.client = client
        self.tools_set = list(tools_set or [])
        self.messages = messages or []
        self.records = records or [
            SimpleMessage.from_thread_message(m) for m in self.messages
        ]
        self.debug = debug

    @override
    def on_event(self, event: "AssistantStreamEvent"):
        """
        Process incoming assistant stream events.

        Specifically handles 'thread.run.requires_action' events that contain tool calls
        requiring execution. Other event types are ignored.

        Notes
        -----
        - Only processes events with 'requires_action' status
        - Extracts run ID and delegates to handle_requires_action
        - Thread-safe event processing
        """

        # Retrieve events that are denoted with 'requires_action'
        # since these will have our tool_calls
        if event.event == "thread.run.requires_action":
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)

    @override
    def on_message_created(self, message: Message) -> None:
        """
        Handle newly created messages in the thread.

        Adds new messages to the internal record keeping system by converting them
        to SimpleMessage format for consistent tracking.
        """

        self.records.append(SimpleMessage.from_thread_message(message))

    @override
    def on_message_done(self, message: Message) -> None:
        """
        Process completed messages in the thread.

        Updates both messages list and records with completed message content.
        Ensures message history is properly maintained with final content.

        Notes
        -----
        - Updates internal message history
        - Updates corresponding record with completed content
        - Maintains message ordering and completeness
        """

        self.messages.append(message)
        for record in self.records[::-1]:
            if record.id == message.id:
                record.set_completed_content(
                    SimpleMessage.from_thread_message(message).content
                )
                break

    def handle_requires_action(self, data: "Run", run_id: typing.Text) -> None:
        """
        Process required actions from the assistant API.

        Executes multiple tool calls concurrently using a ThreadPoolExecutor and
        collects their outputs for submission back to the API.

        Notes
        -----
        - Handles concurrent execution of multiple tool calls
        - Uses ThreadPoolExecutor for parallel processing
        - Maintains thread safety during execution
        - Collects and aggregates tool outputs
        """

        if data.required_action is None:
            return

        tool_outputs: typing.List[ToolOutput] = []
        total_tool_calls = len(data.required_action.submit_tool_outputs.tool_calls)

        logger.debug(f"Required action functions tool calls: {total_tool_calls}")

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=total_tool_calls
        ) as executor:
            futures = [
                executor.submit(
                    run_func_tool_call,
                    tool_call,
                    tools_set=self.tools_set,
                    records=self.records,
                )
                for tool_call in data.required_action.submit_tool_outputs.tool_calls
            ]
            for future in concurrent.futures.as_completed(futures):
                tool_output = future.result()
                tool_outputs.append(tool_output)

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(
        self,
        tool_outputs: typing.Iterable[ToolOutput],
        run_id: typing.Text,
    ) -> None:
        """
        Submit tool outputs back to the OpenAI API.

        Creates a new stream for submitting tool outputs and handles the response
        using a new instance of the event handler.

        Notes
        -----
        - Creates new event handler instance for output submission
        - Maintains state consistency across submissions
        - Handles streaming response until completion
        """

        if self.current_run is None:
            return

        # Use the submit_tool_outputs_stream helper
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=self.__class__(
                self.client,
                tools_set=self.tools_set,
                messages=self.messages,
                records=self.records,
                debug=self.debug,
            ),
        ) as stream:
            stream.until_done()
