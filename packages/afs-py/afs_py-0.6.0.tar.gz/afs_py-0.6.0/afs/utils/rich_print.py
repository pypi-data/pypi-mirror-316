import json
import typing

from pydantic import BaseModel
from rich.table import Table

from afs.config import console

if typing.TYPE_CHECKING:
    from openai.types.beta.threads import Message
    from openai.types.shared.function_definition import FunctionDefinition

    from afs.types.simple_message import SimpleMessage


def dict_table(
    input_dict: typing.Dict | BaseModel,
    *,
    title: typing.Text = "Dictionary Contents",
    width: int = 120,
) -> None:
    """Print a dictionary as a table.

    Example
    -------
    ```python
    my_dict = {
        "name": "Alice",
        "age": 30,
        "languages": ["English", "Spanish"],
        "details": {"height": 170, "weight": 65},
    }
    dict_table(my_dict)
    ```
    """

    console.print("")

    # Create a console and table instance
    table = Table(title=title, width=width)

    # Add two columns: one for keys and one for values
    table.add_column("Key", style="bold magenta")
    table.add_column("Value", style="bold cyan")

    # Iterate over the dictionary and add rows to the table
    for key, value in (
        json.loads(input_dict.model_dump_json())
        if isinstance(input_dict, BaseModel)
        else input_dict
    ).items():
        cell_key = str(key)
        if isinstance(value, typing.Text):
            cell_value = value
        else:
            # Convert value to a JSON string
            try:
                cell_value = json.dumps(value, ensure_ascii=False)
            except Exception:
                cell_value = str(value)
        table.add_row(cell_key, cell_value)

    # Print the table
    console.print(table)
    return None


def function_definition_table(
    func_def: "FunctionDefinition", *, width: int = 120
) -> None:
    """Print a function definition as a table."""

    # Print a header about the function
    dict_table(
        {"name": func_def.name, "description": func_def.description},
        title=f"Function '{func_def.name}'",
        width=width,
    )

    # Pretty-print the parameters:
    if func_def.parameters and func_def.parameters.get("properties"):
        _parameters: typing.Dict[typing.Text, typing.Any] = func_def.parameters[
            "properties"
        ]  # type: ignore
        table = Table(
            title=f"Function '{func_def.name}' Arguments",
            show_header=True,
            header_style="bold magenta",
            width=width,
        )
        table.add_column("Name", style="bold", no_wrap=True)
        table.add_column("Type", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Required", style="yellow")

        required_fields = set(func_def.parameters.get("required") or [])  # type: ignore

        for param_name, param_schema in _parameters.items():
            if "anyOf" in param_schema:
                param_type = ",".join(
                    [arg["type"] for arg in param_schema["anyOf"] if "type" in arg]
                )
            elif "type" in param_schema:
                param_type = param_schema["type"]
            elif "$ref" in param_schema:
                param_type = param_schema["$ref"]
            else:
                param_type = "N/A"
            param_desc = param_schema.get("description", "")
            is_required = "Yes" if param_name in required_fields else "No"

            table.add_row(param_name, param_type, param_desc, is_required)

        console.print(table)
    else:
        console.print("[italic dim]No parameters defined.[/italic dim]")


def messages_table(
    messages: typing.List[typing.Union["SimpleMessage", "Message", typing.Dict]],
    *,
    title: typing.Text = "Messages",
    width: int = 160,
) -> None:
    """Print a simple message as a table."""

    from openai.types.beta.threads import Message

    from afs.types.simple_message import SimpleMessage

    console.print("")

    table = Table(title=title, width=width)
    table.add_column("ID", style="bold magenta")
    table.add_column("Role", style="bold cyan")
    table.add_column("Content", style="green")
    table.add_column("Time Cost", style="yellow")

    for message in messages:
        _message: SimpleMessage
        if isinstance(message, SimpleMessage):
            _message = message.model_copy(deep=True)
        elif isinstance(message, Message):
            _message = SimpleMessage.from_thread_message(message)
        else:
            _message = SimpleMessage.model_validate(message)

        table.add_row(
            _message.id,
            _message.role,
            _message.content,
            f"{_message.time_cost:.2f}s",
        )

    console.print(table)
    return None
