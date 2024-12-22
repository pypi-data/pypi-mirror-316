import time
import typing

import pydantic

if typing.TYPE_CHECKING:
    from openai.types.beta.threads import Message


class SimpleMessage(pydantic.BaseModel):
    id: typing.Optional[typing.Text] = pydantic.Field(default=None)
    role: typing.Optional[typing.Text] = pydantic.Field(default=None)
    content: typing.Text = pydantic.Field(default="")
    created_at: float = pydantic.Field(default_factory=time.time)
    completed_at: typing.Optional[float] = pydantic.Field(default=None)

    @classmethod
    def from_thread_message(cls, message: "Message") -> "SimpleMessage":
        if not message.content:
            content = ""
        elif message.content[0].type == "text":
            content = message.content[0].text.value
        elif message.content[0].type == "refusal":
            content = message.content[0].refusal
        elif message.content[0].type == "image_url":
            content = message.content[0].image_url.url
        elif message.content[0].type == "image_file":
            content = message.content[0].image_file.file_id
        else:
            content = ""
        return cls(
            id=message.id,
            role=message.role,
            content=content,
            created_at=message.created_at,
            completed_at=message.completed_at,
        )

    @property
    def time_cost(self) -> float:
        if self.completed_at is None:
            return 0.0
        return self.completed_at - self.created_at

    def set_completed_content(
        self, content: typing.Text, concatenate: bool = True
    ) -> None:
        self.completed_at = time.time()
        if concatenate:
            self.content = self.content + content
        else:
            self.content = content
