"""
Control logging for the app
"""

import logging
import os
import sys
import threading
import time
from datetime import datetime
from logging import FileHandler
from pathlib import Path

from .baseservice import BaseService
from .config.models import ConfigLogging

LOG_DIR = "log"


class LoggingService(BaseService):
    """_summary_"""

    def __init__(self, config: ConfigLogging):
        super().__init__()

        self._config: ConfigLogging = config

        # ensure dir exists
        os.makedirs(LOG_DIR, exist_ok=True)

        ## formatter ##
        fmt = "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
        log_formatter = logging.Formatter(fmt=fmt)

        # filename per day to log to
        logfile = Path(LOG_DIR, f"node_{datetime.now().astimezone().strftime('%Y%m%d')}.log")

        ## basic configuration
        # latest basicConfig adds a streamHandler output to console if not automatically called
        # earlier by some .warn .info or other
        # force=False because otherwise the pytest console logger stream handler gets deleted
        logging.basicConfig(level=logging.DEBUG, format=fmt, force=False, encoding="utf-8")

        ## logger
        # default logger (root = None or "")
        # root logger also to be the template for all other loggers,
        # that are created in the app at a later time during run
        root_logger = logging.getLogger(name=None)

        # set level based on users config
        root_logger.setLevel(self._config.level)

        ## handler

        self.file_handler = FileHandler(filename=logfile, mode="a", encoding="utf-8", delay=True)
        self.file_handler.setFormatter(log_formatter)

        ## wire logger and handler ##
        root_logger.addHandler(self.file_handler)

        ## mute other loggers
        self.other_loggers()

        ## add the exepthooks
        sys.excepthook = self._handle_sys_exception
        threading.excepthook = self._handle_threading_exception
        # no solution to handle exceptions in sep processes yet...

        self.remove_old_logs()

    def remove_old_logs(self):
        DAYS = 7
        critical_time = DAYS * 86400  # 7 days

        now = time.time()

        for item in Path(LOG_DIR).glob("*.log"):
            if item.is_file():
                if item.stat().st_mtime < (now - critical_time):
                    logging.info(f"deleting logfile older than {DAYS} days: {item}")
                    os.remove(item)

    def other_loggers(self):
        """mute some logger by rasing their log level"""

        for name in [
            "picamera2.picamera2",
            "sse_starlette.sse",
            "PIL.PngImagePlugin",
            "PIL.TiffImagePlugin",
            "multipart",
            "v4l2py",
            "requests",
            "urllib3",
        ]:
            # mute some other logger, by raising their debug level to INFO
            lgr = logging.getLogger(name=name)
            lgr.setLevel(logging.INFO)
            lgr.propagate = True

        os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

    def uvicorn(self):
        """_summary_"""

        for name in [
            "uvicorn.error",
            "uvicorn.access",
            "uvicorn",
        ]:
            lgr = logging.getLogger(name=name)
            lgr.setLevel(self._config.level)
            lgr.propagate = False
            lgr.handlers = [
                logging.root.handlers[0],  # this is the streamhandler if not in pytest.
                self.file_handler,
                self.eventstream_handler,
            ]

    @staticmethod
    def _handle_sys_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logging.getLogger(name="__main__").exception(
            f"Uncaught exception: {exc_type} {exc_value}",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    @staticmethod
    def _handle_threading_exception(args: threading.ExceptHookArgs):
        # report the failure
        logging.getLogger(name="__main__").exception(
            f"Uncaught exception in thread {args.thread}: {args.exc_type} {args.exc_value}",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )
