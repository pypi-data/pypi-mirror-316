import os
import typing
import zoneinfo
from datetime import datetime

import rich.style
import rich.text

from afs.config import console, logger

if typing.TYPE_CHECKING:
    from openai.types.beta.threads import Message


def display_datetime_now(
    tz: zoneinfo.ZoneInfo | typing.Text = zoneinfo.ZoneInfo(os.getenv("TZ") or "UTC"),
) -> typing.Text:
    """
    Format current datetime in a human-readable format with timezone information.

    Generates a formatted string containing the current date and time, including day name,
    month, date, year, time in 12-hour format, timezone name, and UTC offset.

    Notes
    -----
    - Uses system timezone if TZ environment variable is set, otherwise defaults to UTC
    - Format example: "Monday, January 1, 2024 12:00 PM (UTC, UTC+0000)"
    """  # noqa: E501

    tz = zoneinfo.ZoneInfo(tz) if isinstance(tz, typing.Text) else tz
    now = datetime.now(tz)
    return now.strftime("%A, %B %d, %Y %I:%M %p (%Z, UTC%z)")


def display_thread_message(
    message: "Message",
    *,
    tz: zoneinfo.ZoneInfo = zoneinfo.ZoneInfo(os.getenv("TZ", "UTC")),
    is_print: bool = True,
) -> rich.text.Text:
    """
    Format and optionally print an OpenAI thread message with rich text styling.

    Creates a styled text output containing timestamp, message ID, role, and content
    with appropriate color coding. Supports both immediate console output and
    return-only modes.

    Notes
    -----
    - Uses rich text formatting with color-coded components
    - Timestamp: bright_green
    - Message ID: bright_blue
    - Role: bright_magenta
    - Content: default style
    """  # noqa: E501

    output = rich.text.Text("")
    output += rich.text.Text(
        datetime.fromtimestamp(
            message.completed_at or message.created_at, tz
        ).isoformat(),
        style="bright_green",
    )
    output += rich.text.Text(" ", style="default")
    output += rich.text.Text(message.id, style="bright_blue")
    output += rich.text.Text(" ", style="default")
    output += rich.text.Text(f"{message.role:9}:", style="bright_magenta")
    output += rich.text.Text(" ", style="default")
    output += rich.text.Text(
        "".join(
            (
                content_block.text.value
                if content_block.type == "text"
                else str(content_block)
            )
            for content_block in message.content
        ).strip(),
        style="default",
    )

    if is_print:
        console.print(output)

    return output


def display_timezone(
    tz: zoneinfo.ZoneInfo | typing.Text = zoneinfo.ZoneInfo(os.getenv("TZ") or "UTC"),
    *,
    is_print: bool = False,
) -> rich.text.Text:
    """
    Format timezone information as styled rich text.

    Creates a bright green colored text representation of the timezone. Supports
    both ZoneInfo objects and string inputs, with optional console output.

    Notes
    -----
    - Returns timezone string in bright_green color
    - Defaults to system timezone or UTC if not specified
    """  # noqa: E501

    output = rich.text.Text(str(tz), style="bright_green")

    if is_print:
        console.print(output)

    return output


def display_language(
    language: typing.Text,
    display_locale: typing.Text = "en",
    *args,
    **kwargs,
) -> typing.Text:
    """
    Convert language code or name to a standardized display format.

    Processes various language input formats (ISO codes, locale strings, language names)
    and returns a standardized language display name. Supports multiple parsing methods
    and fallback strategies.

    Notes
    -----
    - Handles ISO 639-1, ISO 639-3, and locale codes
    - Normalizes input by converting underscores to hyphens
    - Supports both language-only and language-region formats
    - Falls back to "Unknown language" if parsing fails

    Examples
    --------
    >>> display_language("zh-TW")
    'Chinese (traditional, taiwan)'
    >>> display_language("en_US")
    'English (united states)'
    """  # noqa: E501

    import pycountry
    from babel import Locale, UnknownLocaleError

    # Normalize the input
    language = language.strip()
    # Replace underscores with hyphens for consistency
    language = language.replace("_", "-")
    parts = language.split("-")

    if len(parts) == 2:
        # If input has language and region, format accordingly
        lang_part = parts[0].lower()
        region_part = parts[1].upper()
        input_normalized = f"{lang_part}-{region_part}"
    else:
        # If input is a single part, just lowercase it
        input_normalized = language.lower()

    # Attempt 1: Parse as a locale code using Babel, specifying sep='-'
    try:
        locale_obj = Locale.parse(input_normalized, sep="-")
        display_name = locale_obj.get_display_name(display_locale).capitalize()
        return display_name
    except UnknownLocaleError:
        pass  # Proceed to other parsing methods
    except Exception as e:
        logger.error(f"Error parsing locale: {e}")
        pass

    # Attempt 2: Parse as a language code (ISO 639-1 or ISO 639-3) using pycountry
    pycountry_language = None
    # Try ISO 639-1 (two-letter codes)
    pycountry_language = pycountry.languages.get(alpha_2=input_normalized)
    if not pycountry_language:
        # Try ISO 639-3 (three-letter codes)
        pycountry_language = pycountry.languages.get(alpha_3=input_normalized)
    if pycountry_language:
        # Some languages have multiple names; use the first one
        language_name = pycountry_language.name
        # Handle cases where language names have commas or additional info
        # For example, 'Chinese, Mandarin' -> 'Chinese'
        language_simple = language_name.split(",")[0]
        return language_simple

    # Attempt 3: Check if the input is already a language name
    languages = list(pycountry.languages)
    for lang in languages:
        if hasattr(lang, "name") and lang.name.lower() == input_normalized.lower():
            return lang.name  # Return the standardized language name

    # If all attempts fail, return Unknown
    return "Unknown language"


if __name__ == "__main__":
    console.print(display_language("zh-TW"))
    console.print(display_language("zh_tw"))
    console.print(display_language("zh-tw"))
    console.print(display_language("en_US"))
