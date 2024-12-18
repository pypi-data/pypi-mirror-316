# Copyright 2024 Marimo. All rights reserved.
from __future__ import annotations

import os
import re
from typing import Optional

import uvicorn

import marimo._server.api.lifespans as lifespans
from marimo._config.manager import get_default_config_manager
from marimo._runtime.requests import SerializedCLIArgs
from marimo._server.file_router import AppFileRouter
from marimo._server.main import create_starlette_app
from marimo._server.model import SessionMode
from marimo._server.sessions import LspServer, SessionManager
from marimo._server.tokens import AuthToken
from marimo._server.utils import (
    find_free_port,
    initialize_asyncio,
    initialize_fd_limit,
)
from marimo._server.uvicorn_utils import initialize_signals
from marimo._utils.paths import import_files

DEFAULT_PORT = 2718
PROXY_REGEX = re.compile(r"^(.*):(\d+)$")


def _resolve_proxy(
    port: int, host: str, proxy: Optional[str]
) -> tuple[int, str]:
    """Provided that there is a proxy, utilize the host and port of the proxy.

    -----------------         Communication has to be consistent
    |   User        | ----    so Starlette only needs to know the
    -----------------     |   external facing endpoint, while uvi-
                          |   corn handles the actual running of
                          v   the app.
                  -----------------
      e.g. nginx  |   Proxy       |
                  -----------------
                          |
                          v
                  -----------------
        the app   |   marimo      |
       (uvicorn)  -----------------


    If the proxy is provided, it will default to port 80. Otherwise if the
    proxy has a port specified, it will use that port.
    e.g. `example.com:8080`
    """
    if not proxy:
        return port, host

    match = PROXY_REGEX.match(proxy)
    # Our proxy has an explicit port defined, so return that.
    if match:
        external_host, external_port = match.groups()
        return int(external_port), external_host

    # A default to 80 is reasonable if a proxy is provided.
    return 80, proxy


def start(
    *,
    file_router: AppFileRouter,
    mode: SessionMode,
    development_mode: bool,
    quiet: bool,
    include_code: bool,
    headless: bool,
    port: Optional[int],
    host: str,
    proxy: Optional[str],
    watch: bool,
    cli_args: SerializedCLIArgs,
    base_url: str = "",
    allow_origins: Optional[tuple[str, ...]] = None,
    auth_token: Optional[AuthToken],
    redirect_console_to_browser: bool,
) -> None:
    """
    Start the server.
    """

    # Find a free port if none is specified
    # if the user specifies a port, we don't try to find a free one
    port = port or find_free_port(DEFAULT_PORT)
    lsp_port = find_free_port(DEFAULT_PORT + 200)  # Add 200 to avoid conflicts

    # This is the path that will be used to read the project configuration
    start_path: Optional[str] = None
    if (single_file := file_router.maybe_get_single_file()) is not None:
        start_path = single_file.path
    elif (directory := file_router.directory) is not None:
        start_path = directory
    else:
        start_path = os.getcwd()

    config_reader = get_default_config_manager(current_path=start_path)

    session_manager = SessionManager(
        file_router=file_router,
        mode=mode,
        development_mode=development_mode,
        quiet=quiet,
        include_code=include_code,
        lsp_server=LspServer(lsp_port),
        user_config_manager=config_reader,
        cli_args=cli_args,
        auth_token=auth_token,
        redirect_console_to_browser=redirect_console_to_browser,
    )

    log_level = "info" if development_mode else "error"

    (external_port, external_host) = _resolve_proxy(port, host, proxy)
    app = create_starlette_app(
        base_url=base_url,
        host=external_host,
        lifespan=lifespans.Lifespans(
            [
                lifespans.lsp,
                lifespans.watcher,
                lifespans.etc,
                lifespans.signal_handler,
                lifespans.logging,
                lifespans.open_browser,
            ]
        ),
        allow_origins=allow_origins,
        enable_auth=not AuthToken.is_empty(session_manager.auth_token),
        lsp_port=lsp_port,
    )

    app.state.port = external_port
    app.state.lsp_port = lsp_port
    app.state.host = external_host

    app.state.headless = headless
    app.state.watch = watch
    app.state.session_manager = session_manager
    app.state.base_url = base_url
    app.state.config_manager = config_reader

    # Resource initialization
    # Increase the limit on open file descriptors to prevent resource
    # exhaustion when opening multiple notebooks in the same server.
    initialize_fd_limit(limit=4096)
    initialize_signals()

    server = uvicorn.Server(
        uvicorn.Config(
            app,
            port=port,
            host=host,
            # TODO: cannot use reload unless the app is an import string
            # although cannot use import string because it breaks the
            # session manager
            # reload=development_mode,
            reload_dirs=(
                [
                    os.path.realpath(
                        str(import_files("marimo").joinpath("_static"))
                    )
                ]
                if development_mode
                else None
            ),
            log_level=log_level,
            # uvicorn times out HTTP connections (i.e. TCP sockets) every 5
            # seconds by default; for some reason breaks the server in
            # mysterious ways (it stops processing requests) in edit mode.
            timeout_keep_alive=300 if mode == SessionMode.RUN else int(1e9),
            # ping the websocket once a second to prevent intermittent
            # disconnections
            ws_ping_interval=1,
            # close the websocket if we don't receive a pong after 60 seconds
            ws_ping_timeout=60,
            timeout_graceful_shutdown=1,
            # Under uvloop, reading the socket we monitor under add_reader()
            # occasionally throws BlockingIOError (errno 11, or errno 35,
            # ...). RUN mode no longer uses a socket (it has no IPC) but EDIT
            # does, so force asyncio.
            loop="asyncio" if mode == SessionMode.EDIT else "auto",
        )
    )
    app.state.server = server

    initialize_asyncio()
    server.run()
