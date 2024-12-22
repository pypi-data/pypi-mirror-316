import typing

import diskcache
import openai
from openai.types.beta.assistant import Assistant

from afs.config import logger, settings

if typing.TYPE_CHECKING:
    import redis


def ensure_assistant(
    assistant_id_or_name: typing.Text,
    client: openai.OpenAI,
    *,
    cache: typing.Union["diskcache.Cache", "redis.Redis"] = settings.local_cache,
    expire: typing.Annotated[int, "Cache expiration time in seconds"] = 15 * 60,
    force: typing.Annotated[bool, "Force to fetch from OpenAI"] = False,
    name: typing.Optional[typing.Text] = None,
    instructions: typing.Optional[typing.Text] = None,
    model: typing.Text = "gpt-4o-mini",
) -> "Assistant":
    from afs.utils.openai_utils.iter_ import iter_assistants

    cache_key = f"openai:assistant:{assistant_id_or_name}"
    # Get from cache
    if force is False:
        might_assistant = cache.get(cache_key)
        if might_assistant:
            logger.debug(f"Get assistant from cache: '{assistant_id_or_name}'")
            assistant = Assistant.model_validate_json(might_assistant)  # type: ignore
            if (name and name != assistant.name) or (
                instructions and instructions != assistant.instructions
            ):
                logger.debug(
                    f"Assistant '{assistant_id_or_name}' is outdated, "
                    + "try to update it from OpenAI"
                )
                assistant = client.beta.assistants.update(
                    assistant.id,
                    name=name or openai.NOT_GIVEN,
                    instructions=instructions or openai.NOT_GIVEN,
                )
                logger.info(f"Update assistant: '{assistant_id_or_name}'")
                cache.set(cache_key, assistant.model_dump_json(), expire)
                logger.debug(f"Cache assistant: '{assistant_id_or_name}'")
            return assistant

    # Get by assistant id
    assistant: typing.Optional[Assistant] = None
    if assistant_id_or_name.startswith("asst_"):  # asst_<name>
        try:
            assistant = client.beta.assistants.retrieve(assistant_id_or_name)
            logger.debug(f"Get assistant from OpenAI: '{assistant_id_or_name}'")
        except openai.NotFoundError:
            logger.debug(
                f"Assistant '{assistant_id_or_name}' not found, try to search by name"
            )

    # Get by name
    if assistant is None:
        for _asst in iter_assistants(client):
            if _asst.name == assistant_id_or_name:
                assistant = _asst
                logger.debug(f"Get assistant from OpenAI: '{assistant_id_or_name}'")
                break

    # Not found
    if assistant is None:
        if not name or not instructions:
            raise ValueError(
                f"Assistant '{assistant_id_or_name}' not found, "
                + "or please provide `name` and `instructions` to create it."
            )
        assistant = client.beta.assistants.create(
            model=model,
            name=name,
            instructions=instructions,
        )
        logger.info(f"Create assistant: '{assistant_id_or_name}'")
    # Update assistant if `name` or `instructions` is provided
    else:
        if (name and name != assistant.name) or (
            instructions and instructions != assistant.instructions
        ):
            assistant = client.beta.assistants.update(
                assistant.id,
                name=name or openai.NOT_GIVEN,
                instructions=instructions or openai.NOT_GIVEN,
            )
            logger.info(f"Update assistant: '{assistant_id_or_name}'")

    # Cache
    if cache is not None:
        cache.set(cache_key, assistant.model_dump_json(), expire)
        logger.debug(f"Cache assistant: '{assistant_id_or_name}'")

    return assistant
