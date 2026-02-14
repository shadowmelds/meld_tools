# my_addon/log.py
import typing
from logging import Logger

from bpy.types import Operator


def log_report(
    operator: Operator,
    logger: Logger,
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
