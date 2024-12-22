from typing import TYPE_CHECKING, ClassVar, Type

from openai.types.beta.function_tool import FunctionTool
from openai.types.beta.function_tool_param import FunctionToolParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.shared.function_definition import FunctionDefinition

if TYPE_CHECKING:
    from afs._afs._base_model import AfsBaseModel
    from afs.types.chat_completion_tool import ChatCompletionTool


class AfsFunctionDefinitionDescriptor:
    def __get__(
        self, instance: None, owner: Type["AfsBaseModel"]
    ) -> "FunctionDefinition":
        if instance is not None:
            raise AttributeError(
                f"Class property `{self.__class__.__name__}.function_definition` "
                + "cannot be accessed via an instance."
            )
        import afs.utils.function_definition

        return afs.utils.function_definition.from_base_model(owner)


class AfsChatCompletionToolDescriptor:
    def __get__(
        self, instance: None, owner: Type["AfsBaseModel"]
    ) -> "ChatCompletionTool":
        if instance is not None:
            raise AttributeError(
                f"Class property `{self.__class__.__name__}.chat_completion_tool` "
                + "cannot be accessed via an instance."
            )
        from afs.types.chat_completion_tool import ChatCompletionTool

        return ChatCompletionTool.model_validate(
            {"function": owner.function_definition}
        )


class AfsChatCompletionToolParamDescriptor:
    def __get__(
        self, instance: None, owner: Type["AfsBaseModel"]
    ) -> "ChatCompletionToolParam":
        if instance is not None:
            raise AttributeError(
                "Class property "
                + f"`{self.__class__.__name__}.chat_completion_tool_param` "
                + "cannot be accessed via an instance."
            )
        return owner.chat_completion_tool.model_dump(exclude_none=True)  # type: ignore


class AfsFunctionToolDescriptor:
    def __get__(self, instance: None, owner: Type["AfsBaseModel"]) -> "FunctionTool":
        if instance is not None:
            raise AttributeError(
                f"Class property `{self.__class__.__name__}.function_tool` "
                + "cannot be accessed via an instance."
            )
        import afs.utils.function_tool

        return afs.utils.function_tool.from_base_model(owner)


class AfsFunctionToolParamDescriptor:
    def __get__(
        self, instance: None, owner: Type["AfsBaseModel"]
    ) -> "FunctionToolParam":
        if instance is not None:
            raise AttributeError(
                "Class property "
                + f"`{self.__class__.__name__}.function_tool_param` "
                + "cannot be accessed via an instance."
            )
        return owner.function_tool.model_dump(exclude_none=True)  # type: ignore


class AfsDescriptors:
    function_definition: ClassVar[AfsFunctionDefinitionDescriptor] = (
        AfsFunctionDefinitionDescriptor()
    )
    chat_completion_tool: ClassVar[AfsChatCompletionToolDescriptor] = (
        AfsChatCompletionToolDescriptor()
    )
    chat_completion_tool_param: ClassVar[AfsChatCompletionToolParamDescriptor] = (
        AfsChatCompletionToolParamDescriptor()
    )
    function_tool: ClassVar[AfsFunctionToolDescriptor] = AfsFunctionToolDescriptor()
    function_tool_param: ClassVar[AfsFunctionToolParamDescriptor] = (
        AfsFunctionToolParamDescriptor()
    )
