# pylint: disable=protected-access, too-many-lines
"""Main module of kytos/listen_events Kytos Network Application.

NApp to listen and broadcast events.
"""
import os
import requests
from napps.kytos.listen_events import settings # pylint: disable=E0401
from kytos.core import KytosNApp, log, rest
from kytos.core.events import KytosEvent
from kytos.core.helpers import listen_to
from kytos.core.rest_api import (HTTPException, JSONResponse, Request,
                                 content_type_json_or_415, get_json_or_400)

# pylint: disable=too-many-public-methods
class Main(KytosNApp):
    """Main class of amlight/listen_events NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Replace the '__init__' method for the KytosNApp subclass.

        The setup method is automatically called by the controller when your
        application is loaded.

        So, if you have any setup routine, insert it here.
        """
        self.event_info = {}  # pylint: disable=W0201
        self.shelve_loaded = False  # pylint: disable=W0201
        self.version_control = False  # pylint: disable=W0201
        OXPO_ID = int(os.environ.get("OXPO_ID"))

    def execute(self):
        """Execute once when the napp is running."""
        if self._lock.locked():
            return
        log.debug("Starting consistency routine")
        with self._lock:
            self.execute_consistency()
        log.debug("Finished consistency routine")
        self.load_shelve()

   def shutdown(self):
        """Run when your NApp is unloaded.

        If you have some cleanup procedure, insert it here.
        """

    def load_shelve(self):  # pylint: disable=W0613
        """Function meant for validation, to make sure that the store_shelve
        has been loaded before all the other functions that use it begins to
        call it."""
        if not self.shelve_loaded:  # pylint: disable=E0203
            with shelve.open("events_shelve") as events_shelve:
                events_shelve['events'] = []
                events_shelve.close()
                self.shelve_loaded = True  # pylint: disable=W0201
                open_shelve.close()

    @listen_to(
            "kytos/topology.link_*",
            "kytos/topology.switch.*",
            pool="dynamic_single")
    def listen_event(self, event=None):
        """Function meant for listen topology"""
        if event is not None and self.version_control:
            dpid = ""
            if event.name in settings.ADMIN_EVENTS:
                switch_event = {
                        "version/control.initialize": True,
                        "kytos/topology.switch.enabled": True,
                        "kytos/topology.switch.disabled": True
                        }
                if switch_event.get(event.name, False):
                    event_type = "administrative"
                    dpid = event.content["dpid"]
                else:
                    event_type = None
            elif event.name in settings.OPERATIONAL_EVENTS and \
                    event.timestamp is not None:
                event_type = "operational"
            else:
                event_type = None
            if event_type is None:
                return {"event": "not action event"}
            # open the event shelve
            with shelve.open("events_shelve") as log_events:
                events_data =
                        {
                            "type": event_type,
                            "timestamp": event.timestamp,
                            "name": event.name,
                            "dpid": dpid
                        }
                shelve_events.append(events_data)
                log_events['events'] = shelve_events
                log_events.close()
            return sdx_lc_response
        return {"event": "not action event"}

    @rest("v1/listen_event", methods=["POST"])
    def get_listen_event(self, request: Request) -> JSONResponse:
        """consume call listen Event"""
        try:
            result = get_json_or_400(request, self.controller.loop)
            name = result.get("name")
            content = result.get("content")
            event = KytosEvent(
                    name=name, content=content)
            # self.controller.buffers.app.put(event)
            event_result = self.listen_event(event)
            return JSONResponse(event_result)
        except requests.exceptions.HTTPError as http_error:
            raise SystemExit(
                    http_error, detail="listen topology fails") from http_error

    @rest("v1/shelve/events", methods=["GET"])
    def get_shelve_events(self, _request: Request) -> JSONResponse:
        """return events shelve"""
        with shelve.open("events_shelve") as open_shelve:
            events = open_shelve['events']
        open_shelve.close()
        return JSONResponse({"events": events})
