# my_addon/log.py
import logging
import typing

from bpy.types import Operator

logger: logging.Logger = logging.getLogger("meld_toos")


def log_report(
    operator: Operator,
    type: set[
        typing.Literal[
            "DEBUG",  # Debug.
            "INFO",  # Info.
            "OPERATOR",  # Operator.
            "PROPERTY",  # Property.
            "WARNING",  # Warning.
            "ERROR",  # Error.
            "ERROR_INVALID_INPUT",  # Invalid Input.
            "ERROR_INVALID_CONTEXT",  # Invalid Context.
            "ERROR_OUT_OF_MEMORY",  # Out of Memory.
        ]
    ],
    msg: str,
) -> None:
    logger.info(msg)
    operator.report(type, msg)
