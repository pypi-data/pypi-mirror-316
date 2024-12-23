"""
Logging configuration store
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypedDict, Union

from loguru import logger
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from loguru import HandlerConfig


class ConfigLike(TypedDict):
    """
    Configuration-like to use with loguru
    """

    handlers: list[HandlerConfig]


LoggingConfigLike: TypeAlias = Union[ConfigLike, None]
LoggingConfigSerialisedType: TypeAlias = Union[
    dict[str, list[dict[str, Union[str, Path]]]], None
]

LOGGING_CONFIG: LoggingConfigLike = None
"""
Logging configuration being used

We provide this as a global variable
so it can be passed to parallel processes.
It's not clear if this is the right pattern,
but we're trying it.
"""


def serialise_logging_config(config: LoggingConfigLike) -> LoggingConfigSerialisedType:
    """
    Serialise logging configuration

    This allows us to pass logging configuration from the main process
    to parallel process workers.
    We're not sure if this is the right pattern, but it is working for now.
    However, we don't know what all the edge cases are here, so bugs are likely.
    If you find one, please raise an issue.

    Parameters
    ----------
    config
        Configuration to serialise

    Returns
    -------
    :
        Serialised configuration
    """
    if config is None:
        res = None

    else:
        new_handlers_l = []
        for handler in config["handlers"]:
            new_handler = {k: v for k, v in handler.items() if k != "sink"}

            if isinstance(handler["sink"], (str, Path)):
                new_handler["sink"] = handler["sink"]

            elif handler["sink"] == sys.stderr or (
                isinstance(handler["sink"], io.TextIOWrapper)
                and (handler["sink"].name == "<stderr>")
            ):
                new_handler["sink"] = "stderr"

            elif handler["sink"] == sys.stdout or (
                isinstance(handler["sink"], io.TextIOWrapper)
                and (handler["sink"].name == "<stdout>")
            ):
                new_handler["sink"] = "stdout"

            else:
                logger.warning(
                    f"Not sure how to serialise {handler['sink']=}, "
                    "your parallel processes may explode"
                )
                new_handler["sink"] = handler["sink"]

            new_handlers_l.append(new_handler)

        res = {k: v for k, v in config.items() if k != "handlers"}
        res["handlers"] = new_handlers_l

    logger.debug(f"Serialised {config} to {res}")
    return res  # type: ignore # making this behave is not trivial


def deserialise_logging_config(
    config: LoggingConfigSerialisedType,
) -> LoggingConfigLike:
    """
    Deserialise logging configuration

    This allows us to load logging configuration from the main process
    in parallel process workers.
    We're not sure if this is the right pattern, but it is working for now.
    However, we don't know what all the edge cases are here, so bugs are likely.
    If you find one, please raise an issue.

    Parameters
    ----------
    config
        Serialised configuration to deserialise

    Returns
    -------
    :
        Deserialised configuration
    """
    if config is None:
        res: LoggingConfigLike = None

    else:
        new_handlers_l = []
        for handler in config["handlers"]:
            new_handler: dict[str, Union[str, Path, io.TextIOWrapper, Any]] = {
                k: v for k, v in handler.items() if k != "sink"
            }

            if handler["sink"] == "stderr":
                logger.debug(f"Deserialising {handler['sink']=} to sys.stderr")
                new_handler["sink"] = sys.stderr

            elif handler["sink"] == "stdout":
                logger.debug(f"Deserialising {handler['sink']=} to sys.stdout")
                new_handler["sink"] = sys.stdout

            else:
                logger.debug(f"Deserialising {handler['sink']=} as is")
                new_handler["sink"] = handler["sink"]

            new_handlers_l.append(new_handler)

        res = {k: v for k, v in config.items() if k != "handlers"}  # type: ignore # making this behave not trivial
        res["handlers"] = new_handlers_l  # type: ignore # making this behave not trivial

    logger.debug(f"Deserialised {config} to {res}")
    return res
