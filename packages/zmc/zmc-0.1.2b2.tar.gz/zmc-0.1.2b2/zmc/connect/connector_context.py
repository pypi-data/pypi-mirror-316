"""ConnectorContext (alias connect) module.

This is the module that provides the easy-to-use ability for users to establish
a connection to the Mission Control app.
"""

import asyncio
import contextvars
import functools
import inspect
import logging


from .connector_config import config
from .mock_connector import MockConnector
from .websocket_client import WebSocketClient

__all__ = ["ConnectorContext", "context_connector"]


# Timeout (s) when waiting for a connection. Scripts running this code are meant
# to run when the app is already open and the corresponding websocket server is
# up and running. This means that it should connect almost immediately, so 3
# seconds should be more than enough.
CONNECTION_TIMEOUT = 3

# User friendly error message regarding timeouts when waiting for a connection.
# Users seeing this are likely running without having the app open, using the
# wrong port, or have multiple runs going on at the same time.
CONNECTION_TIMEOUT_ERROR_MSG = (
    "Unable to establish a connection with the Mission Control app. This could "
    "be happening for a few reasons:"
    "\n   - You are running your script without having the app open"
    "\n   - You are running your script but don't have the corresponding gui "
    "(identified by its id) open in the app"
    "\n   - There is already a script running connected to the same gui"
    "\n   - The port you are using does not match the one the app is serving to"
    "\nIf you are just trying to debug, use `zmc.connect(debug=True)` to mock "
    "out the connection."
)

# User friendly error message regarding multiple connections. Users seeing this
# must be nesting their context or calls to decorated functions.
MULTIPLE_CONNECTIONS_ERROR_MSG = (
    "Cannot create multiple connections at the same time. This is likely "
    "happening because of nested `with` statements or nested calls to "
    "functions decorated with `zmc.connect()`."
)

# Context var containing the Connector object that the context manager starts.
context_connector = contextvars.ContextVar("context_connector", default=None)

_root_logger = logging.getLogger()


class ConnectorContext:
    """Context manager for a connection to the Mission Control app.

    Starts a connection in a separate thread to the one that the manager is
    called in. The context won't start until a connection has been established.
    If no connection is established before the timeout, a RuntimeError will be
    raised.

    Usage as a context manager:
    ```
    import zmc

    with zmc.connect():
        do_something()  # will execute while connection is established.
    ```

    This class supports both synchronous and asynchronous context management. In
    asynchronous contexts, the wait for the connection is done asynchronously so
    it does not prevent other tasks from executing during the wait. It will,
    however, still prevent the context from entering until a connection is made.

    For convenience, instances of this class can also be used as decorators for
    functions. Any function decorated will, when called, first enter a context
    and then execute.

    Usage as decorator:
    ```
    import zmc

    @zmc.connect()
    def do_something():
        ... # arbitrary implementation

    do_something()  # will execute while connection is established.
    ```

    To run the script without requiring a connection to the app, use the
    `debug=True` argument. This will mock out the connection with the Mission
    Control app. No values will be read or sent from the app but the rest of the
    code will work as expected.

    Example:
    ```
    with zmc.connect(debug=True):
        do_something()
    ```

    args: (keyword-only)
        - debug: (default: False). Whether or not to enter the context in
                debugging mode. If true, the connection will be mocked.
        - verbose: (default: False). Whether to enable verbose logging
    """

    def __init__(self, *, debug=False, verbose=False, gui_id=None):
        self._verbose = verbose
        self._prev_logger_level = None
        gui_id = gui_id if gui_id is not None else config.gui_id
        self._connector = (
            WebSocketClient("localhost", config.port, gui_id)
            if not debug
            else MockConnector(gui_id)
        )
        self.contextvar_token = None

    def __call__(self, func):
        # Async case. It is almost identical to the sync one but with a few
        # added "async" and "await" keywords.
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def aconnector_wrapper(*args, **kwargs):
                async with self:
                    await func(*args, **kwargs)

            return aconnector_wrapper

        # Sync case
        @functools.wraps(func)
        def connector_wrapper(*args, **kwargs):
            with self:
                func(*args, **kwargs)

        return connector_wrapper

    def _start_connector_thread(self):
        if context_connector.get() is not None:
            raise RuntimeError(MULTIPLE_CONNECTIONS_ERROR_MSG)
        self.contextvar_token = context_connector.set(self._connector)
        self._connector.start_connector()

    def __enter__(self):
        if self._verbose:
            self._prev_logger_level = _root_logger.level
            _root_logger.setLevel(logging.DEBUG)
        try:
            self._start_connector_thread()
            # Await a connection. Otherwise the zmc code inside the context
            # won't work as intended.
            self._connector.wait_for_connection(CONNECTION_TIMEOUT)
        # TODO: cleaner way of handling exceptions and always exiting?
        except TimeoutError as exc:
            self.__exit__(None, None, None)
            raise RuntimeError(CONNECTION_TIMEOUT_ERROR_MSG) from exc
        except Exception:
            self.__exit__(None, None, None)
            raise
        except SystemExit:
            self.__exit__(None, None, None)

    async def __aenter__(self):
        if self._verbose:
            self._prev_logger_level = _root_logger.level
            _root_logger.setLevel(logging.DEBUG)
        try:
            self._start_connector_thread()
            # Await a connection. Otherwise the zmc code inside the context
            # won't work as intended. Given that this is an async context, the
            # wait happens on another thread to not block other async actions.
            # It will still, however, block the context from entering until the
            # connection happens.
            await asyncio.get_event_loop().run_in_executor(
                None, self._connector.wait_for_connection, CONNECTION_TIMEOUT
            )
        except TimeoutError as exc:
            await self.__aexit__(None, None, None)
            raise RuntimeError(CONNECTION_TIMEOUT_ERROR_MSG) from exc
        except Exception:
            await self.__aexit__(None, None, None)
            raise
        except SystemExit:
            await self.__aexit__(None, None, None)

    # pylint: disable=inconsistent-return-statements
    def __exit__(self, exc_type, exc_value, traceback):
        self._connector.stop_connector()
        context_connector.reset(self.contextvar_token)

        # reset logging level that was being used before entering
        if self._prev_logger_level:
            _root_logger.setLevel(self._prev_logger_level)

        # If an exception was raised in the connector thread, raise that now.
        if self._connector.has_thread_exception():
            self._connector.raise_thread_exception()

        if exc_type is SystemExit:
            return True  # Suppress the SystemExit exception

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.__exit__(exc_type, exc_value, traceback)
