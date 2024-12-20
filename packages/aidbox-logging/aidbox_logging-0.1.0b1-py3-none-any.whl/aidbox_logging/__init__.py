import asyncio
import atexit
import logging.handlers
import queue
import sys
import threading
import traceback
from types import TracebackType
from typing import Self

import requests

__title__ = "aidbox-logging"
__version__ = "0.1.0b1"
__author__ = "beda.software"
__license__ = "MIT"
__copyright__ = "Copyright 2024 beda.software"

# Version synonym
VERSION = __version__


class AidboxLoggyHandler(logging.Handler):
    """This logger collects log in queue and sends them to Aidbox in a parallel thread.

    It allows not to block the main thread.
    """

    def __init__(
        self: Self,
        loggy_url: str,
        app: str,
        version: str,
        meta: dict | None = None,
        *args,  # noqa: ANN002
        **kwargs,  # noqa: ANN003
    ) -> None:
        self.loggy_url = loggy_url
        self.app = app
        self.version = version
        self.meta = meta
        super().__init__(*args, **kwargs)

    def getPayload(  # noqa: N802 the logging module is written using camelCase
        self: Self, record: logging.LogRecord
    ) -> dict:
        message = self.format(record)
        meta = record.__dict__.get("meta", None)
        level = record.levelname

        return {
            "type": f"{self.app}-{level}",
            "v": self.version,
            "message": {
                "message": message,
                "meta": {
                    **(self.meta or {}),
                    **(meta or {}),
                    "version": self.version,
                    "app": self.app,
                    "level": level,
                    "logger": record.name,
                },
            },
        }

    def emit(self: Self, record: logging.LogRecord) -> None:
        urllib3_logger = logging.getLogger("urllib3.connectionpool")
        urllib3_logger.disabled = True
        requests_logger = logging.getLogger("requests")
        requests_logger.disabled = True

        try:
            requests.post(self.loggy_url, json=self.getPayload(record))
        except Exception:
            self.handleError(record)
        finally:
            urllib3_logger.disabled = False
            requests_logger.disabled = False


def enable_excepthook_logging() -> None:
    loop = asyncio.get_event_loop()

    def sys_excepthook(
        etype: type[BaseException], value: BaseException, tb: TracebackType | None
    ) -> None:
        if issubclass(etype, SystemExit):
            return

        message = "".join(traceback.format_exception(etype, value, tb))
        logging.critical(message)

    def asyncio_exception_handler(loop: asyncio.AbstractEventLoop, context: dict) -> None:
        exception = context.get("exception")
        if exception:
            message = "".join(
                traceback.format_exception(type(exception), exception, exception.__traceback__)
            )
            logging.critical(message)
        else:
            logging.error("Unhandled error in asyncio: %s", context["message"])

    def threading_excepthook(args: tuple) -> None:
        sys_excepthook(args[0], args[1], args[2])

    loop.set_exception_handler(asyncio_exception_handler)
    sys.excepthook = sys_excepthook
    threading.excepthook = threading_excepthook


def init_queued_aidbox_loggy_handler(
    loggy_url: str, app: str, version: str, meta: dict | None = None
) -> logging.Handler:
    aidbox_loggy_handler = AidboxLoggyHandler(
        loggy_url,
        app=app,
        version=version,
        meta=meta,
    )
    log_queue: queue.SimpleQueue = queue.SimpleQueue()
    log_queue_handler = logging.handlers.QueueHandler(log_queue)
    log_queue_listener = logging.handlers.QueueListener(log_queue, aidbox_loggy_handler)
    log_queue_listener.start()

    atexit.register(log_queue_listener.stop)

    return log_queue_handler


__all__ = ["enable_exepthook_logging", "init_queued_aidbox_loggy_handler"]
