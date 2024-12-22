import logging
import os
import random
import sys
import typing
from datetime import datetime
from zoneinfo import ZoneInfo

import colorama


def setup_logger(
    *loggers: typing.Text | logging.Logger,
    formatter: typing.Optional[logging.Formatter] = None,
    level: typing.Optional[int] = None,
    fmt: typing.Optional[typing.Text] = None,
    reset_handlers: bool = True,
) -> typing.List[logging.Logger]:
    _loggers = [
        logging.getLogger(name) if isinstance(name, typing.Text) else name
        for name in loggers
    ]

    if reset_handlers:
        for _logger in _loggers:
            _logger.handlers = []

    for _logger in _loggers:
        _logger.setLevel(level or logging.DEBUG)

    # Create formatter similar to uvicorn's default format
    formatter = formatter or ColoredIsoDatetimeFormatter(
        fmt=fmt or "%(asctime)s%(levelname)-10s %(message)s"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    for _logger in _loggers:
        _logger.addHandler(stream_handler)

    return _loggers


class IsoDatetimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        record_datetime = datetime.fromtimestamp(record.created).astimezone(
            ZoneInfo(os.getenv("TZ", "UTC"))
        )
        # Drop microseconds
        record_datetime = record_datetime.replace(microsecond=0)
        return (
            colorama.Fore.BLACK
            + colorama.Back.WHITE
            + f' {record_datetime.strftime("%Y-%m-%dT%H:%M:%S")} '
            + colorama.Style.RESET_ALL
        )


class ColoredIsoDatetimeFormatter(IsoDatetimeFormatter):
    COLORS_FE = {
        "DEBUG": colorama.Fore.BLUE,
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.MAGENTA,
    }
    COLORS_BG = {
        "DEBUG": colorama.Back.BLUE,
        "INFO": colorama.Back.GREEN,
        "WARNING": colorama.Back.YELLOW,
        "ERROR": colorama.Back.RED,
        "CRITICAL": colorama.Back.MAGENTA,
    }
    COLORS_BG_TO_FE = {
        colorama.Back.BLUE: colorama.Fore.BLUE,
        colorama.Back.GREEN: colorama.Fore.GREEN,
        colorama.Back.YELLOW: colorama.Fore.YELLOW,
        colorama.Back.RED: colorama.Fore.RED,
        colorama.Back.MAGENTA: colorama.Fore.MAGENTA,
    }
    MSG_COLORS = {
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "CRITICAL": colorama.Fore.MAGENTA,
        "ERROR": colorama.Fore.RED,
    }
    LEVEL_EMOJI = {
        "DEBUG": "🔍",
        "INFO": "💡",
        "WARNING": "🚸",
        "ERROR": "🚨",
        "CRITICAL": "🔥",
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS_FE and levelname in self.COLORS_BG:
            record.levelname = (
                colorama.Fore.WHITE
                + self.COLORS_BG[levelname]
                + "\uE0B0"
                + self.COLORS_BG[levelname]
                + f" {self.LEVEL_EMOJI[levelname]} {levelname:8s}"
                + colorama.Style.RESET_ALL
                + self.COLORS_BG_TO_FE[self.COLORS_BG[levelname]]
                + "\uE0B0"
                + colorama.Style.RESET_ALL
            )
        record.name = (
            colorama.Fore.LIGHTBLUE_EX + record.name + colorama.Style.RESET_ALL
        )
        if not isinstance(record.msg, typing.Text):
            record.msg = str(record.msg)
        if levelname in self.MSG_COLORS:
            record.msg = (
                self.COLORS_FE[levelname] + record.msg + colorama.Style.RESET_ALL
            )
        elif levelname == "DEBUG":
            pass
        else:
            styled_text = ""
            for char in record.msg:
                styled_text += (
                    random.choice(
                        (
                            colorama.Fore.RED,
                            colorama.Fore.GREEN,
                            colorama.Fore.YELLOW,
                            colorama.Fore.BLUE,
                            colorama.Fore.MAGENTA,
                            colorama.Fore.CYAN,
                        )
                    )
                    + char
                )
            record.msg = styled_text + colorama.Style.RESET_ALL
        return super(ColoredIsoDatetimeFormatter, self).format(record)
