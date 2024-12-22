from typing import TYPE_CHECKING, Any, Text

from openai.types.beta.threads import run_submit_tool_outputs_params
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)

if TYPE_CHECKING:
    from afs.types.chat_completion_tool_message import ChatCompletionToolMessage
    from afs.types.tool_output import ToolOutput


class AfsParser:
    @classmethod
    def parse_content(cls, response: Any) -> Text:
        """
        Convert any response content to a string representation.

        A base implementation that simply converts the input to a string. Subclasses
        can override this method to provide custom parsing logic for specific response
        types.
        """

        return str(response)

    @classmethod
    def parse_content_as_openai_tool_message(
        cls, response: Any, *, tool_call_id: Text
    ) -> "ChatCompletionToolMessage":
        """
        Parse response content into an OpenAI chat completion tool message format.

        Creates a structured tool message containing the parsed content and tool call ID
        for use in chat completions. The content is first processed through parse_content()
        before being wrapped in the message structure.

        Notes
        -----
        This method requires the tool_call_id to be provided as a keyword argument to
        ensure proper message construction.
        """  # noqa: E501

        from afs.types.chat_completion_tool_message import ChatCompletionToolMessage

        return ChatCompletionToolMessage.model_validate(
            {
                "content": cls.parse_content(response),
                "tool_call_id": tool_call_id,
            }
        )

    @classmethod
    def parse_content_as_openai_tool_message_param(
        cls, response: Any, *, tool_call_id: Text
    ) -> ChatCompletionToolMessageParam:
        """
        Convert response content into an OpenAI tool message parameter format.

        A convenience method that builds upon parse_content_as_openai_tool_message()
        to create a parameter-ready format for OpenAI API calls, excluding any None
        values from the output.
        """

        return cls.parse_content_as_openai_tool_message(
            response, tool_call_id=tool_call_id
        ).model_dump(
            exclude_none=True
        )  # type: ignore

    @classmethod
    def parse_content_as_assistant_tool_output(
        cls, response: Any, *, tool_call_id: Text
    ) -> "ToolOutput":
        """
        Parse response content into an assistant tool output format.

        Creates a structured tool output containing the parsed content and tool call ID
        for use with OpenAI's assistant API. The content is first processed through
        parse_content() before being wrapped in the output structure.

        Notes
        -----
        This method requires the tool_call_id to be provided as a keyword argument to
        ensure proper output construction.
        """  # noqa: E501

        from afs.types.tool_output import ToolOutput

        return ToolOutput.model_validate(
            {
                "output": cls.parse_content(response),
                "tool_call_id": tool_call_id,
            }
        )

    @classmethod
    def parse_content_as_assistant_tool_output_param(
        cls, response: Any, *, tool_call_id: Text
    ) -> "run_submit_tool_outputs_params.ToolOutput":
        """
        Convert response content into an assistant tool output parameter format.

        A convenience method that builds upon parse_content_as_assistant_tool_output()
        to create a parameter-ready format for OpenAI Assistant API calls, excluding
        any None values from the output.
        """  # noqa: E501

        return cls.parse_content_as_assistant_tool_output(
            response, tool_call_id=tool_call_id
        ).model_dump(
            exclude_none=True
        )  # type: ignore
