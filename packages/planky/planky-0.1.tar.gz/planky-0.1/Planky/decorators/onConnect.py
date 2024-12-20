from collections.abc import Callable

from Planky import listeners
from Planky.base.server import Server


class OnConnect:

    def on_connect(self, filter: Callable = None) -> Callable:
        """
        **Decorator!** Register callback on connect event

        :param filter: function to filter events
        """
        def decorator(func: Callable) -> Callable:
            if isinstance(self, Server):
                self.handler.add_listener(listeners.OnConnect(func, filter))

            return func

        return decorator