"""kytos/pong."""

import os
from kytos.core import KytosEvent, KytosNApp, log
from kytos.core.helpers import listen_to
from threading import Lock


class Main(KytosNApp):
    """Main class to be used by Kytos controller."""

    def setup(self):
        """Replace the 'init' method for the KytosApp subclass.

        The setup method is automatically called by the run method.
        Users shouldn't call this method directly.
        """
        log.info("pong starting")
        self.execute_as_loop(10)
        self._lock = Lock()
        self._count = 0
        self._reply_skip_count = int(os.environ.get("PONG_SKIP_COUNT", 1000))

        # TODO try out a async decorator

    @listen_to("kytos/ping.request")
    def on_ping(self, event):
        """On ping."""
        event_name = "kytos/pong.reply"
        with self._lock:
            self._count += 1
            if self._reply_skip_count > 0 and self._count % self._reply_skip_count != 0:
                return
        event = KytosEvent(name=event_name, content=dict(event.content))
        log.debug(f"on_ping sub replied to {event.content}")
        self.controller.buffers.app.put(event)
        with self._lock:
            self._count = 0

    def execute(self):
        """Run once on NApp 'start' or in a loop.

        The execute method is called by the run method of KytosNApp class.
        Users shouldn't call this method directly.
        """
        pass

    def shutdown(self):
        """Shutdown routine of the NApp."""
        log.debug("pong stopping")
