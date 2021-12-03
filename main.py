"""kytos/pong."""

from kytos.core import KytosEvent, KytosNApp, log
from kytos.core.helpers import listen_to


class Main(KytosNApp):
    """Main class to be used by Kytos controller."""

    def setup(self):
        """Replace the 'init' method for the KytosApp subclass.

        The setup method is automatically called by the run method.
        Users shouldn't call this method directly.
        """
        log.info("pong starting")
        self.execute_as_loop(10)

        # TODO try out a async decorator

    @listen_to("kytos/ping.request")
    def on_ping(self, event):
        """On ping."""
        log.debug(f"on_ping sub {event.content}")
        event_name = "kytos/pong.reply"
        event = KytosEvent(name=event_name, content=dict(event.content))
        self.controller.buffers.app.put(event)

    def execute(self):
        """Run once on NApp 'start' or in a loop.

        The execute method is called by the run method of KytosNApp class.
        Users shouldn't call this method directly.
        """
        pass

    def shutdown(self):
        """Shutdown routine of the NApp."""
        log.debug("pong stopping")
