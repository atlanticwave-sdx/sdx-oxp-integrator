# pylint: disable=protected-access, too-many-lines
"""Main module of kytos/mq_consumer Kytos Network Application.

NApp to consume messages from rabittmq.
"""
import asyncio
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
import pathlib
import time
import traceback
from collections import defaultdict
from threading import Lock
from typing import Optional

from pydantic import ValidationError

from kytos.core import KytosNApp, log, rest
from kytos.core.events import KytosEvent
from kytos.core.exceptions import KytosTagError
from kytos.core.helpers import (alisten_to, listen_to, load_spec, now,
                                validate_openapi)
from kytos.core.rest_api import (HTTPException, JSONResponse, Request,
                                 get_json_or_400)
from napps.kytos.mq-consumer import settings


# pylint: disable=too-many-public-methods
class Main(KytosNApp):
    """Main class of amlight/mq_consumer NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Replace the '__init__' method for the KytosNApp subclass.

        The setup method is automatically called by the controller when your
        application is loaded.

        So, if you have any setup routine, insert it here.
        """

    def execute(self):
        """Execute once when the napp is running."""
        if self._lock.locked():
            return
        log.debug("Starting consistency routine")
        with self._lock:
            self.execute_consistency()
        log.debug("Finished consistency routine")

