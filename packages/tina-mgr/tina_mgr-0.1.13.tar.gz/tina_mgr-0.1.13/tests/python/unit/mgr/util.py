# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Helper functions for testing tina using tmux."""

from __future__ import annotations

import contextlib
import dataclasses
import shlex
import time
import typing

import libtmux
import pytest

from unit import util as t_util


if typing.TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterator
    from typing import Final, Self


@dataclasses.dataclass(frozen=True)
class Tina:
    """An instance of tina spawned in a tmux session."""

    home: pathlib.Path
    """The home directory that tina sees."""

    srv: libtmux.Server
    """The tmux server spawned for this occassion."""

    pane: libtmux.Pane
    """The tmux pane that tina runs in."""

    def assert_text_at(self, x: int, y: int, text: str) -> None:
        """Make sure the pane contains the specified characters at the specified position."""
        print(f"Checking for {text!r} at ({x}, {y})")
        assert self.srv.is_alive()
        if not text:
            return

        lines: Final = self.pane.capture_pane()
        assert len(lines) > y
        line: Final = lines[y]
        assert len(line) > x
        assert line[x : x + len(text)] == text
        print("- got it")

    def assert_no_text_at(self, x: int, y: int) -> None:
        """Make sure there's nothing from the specified position to the end of the line."""
        print(f"Checking for nothing at ({x}, {y})")
        assert self.srv.is_alive()

        lines: Final = self.pane.capture_pane()
        if len(lines) < y + 1:
            return
        line: Final = lines[y]
        assert len(line) <= x
        print("- got it")

    def assert_stopped(self, *, timeout_sec: int = 2) -> None:
        """Wait for the specified number of seconds for the server to go away."""
        print(f"Waiting for up to {timeout_sec} seconds for the server to go away")
        for _ in range(timeout_sec * 2):
            if not self.srv.is_alive():
                print("- gone away")
                return

            time.sleep(0.1)

        pytest.fail(f"The server at {self.srv.socket_path} did not go away")

    def quit(self) -> None:
        """Send 'q', wait for `tina` to go away."""
        print("Sending 'q'")
        self.pane.send_keys("q", enter=False, literal=True)
        self.assert_stopped()

    @classmethod
    @contextlib.contextmanager
    def spawn_tina(cls, home: pathlib.Path, prog: pathlib.Path) -> Iterator[Self]:
        """Spawn tina in a tmux session."""
        env: Final = t_util.get_utf8_env()
        env["HOME"] = str(home)

        socket_path: Final = home / ".tmux.socket"
        srv: Final = libtmux.Server(socket_path=socket_path)
        try:
            print(f"Prepared a tmux server at {socket_path}")
            assert not srv.is_alive()
            assert not srv.sessions

            print(f"Starting a `{prog}` session at {srv.socket_path}")
            sess: Final = srv.new_session(
                "tina",
                window_command=shlex.quote(str(prog)),
                environment=env,
            )
            match srv.sessions:
                case [single] if single == sess:
                    match sess.windows:
                        case [win]:
                            match win.panes:
                                case [pane]:
                                    print("Got a single pane, waiting for a little while")
                                    time.sleep(0.1)
                                    assert srv.is_alive()
                                    res: Final = cls(home=home, srv=srv, pane=pane)
                                    res.assert_text_at(0, 0, "q:Quit")
                                    yield res

                                case other_panes:
                                    pytest.fail(repr((srv, sess, win, other_panes)))

                        case other_windows:
                            pytest.fail(repr((srv, sess, other_windows)))

                case other_sessions:
                    pytest.fail(repr((srv, sess, other_sessions)))
        finally:
            if srv.is_alive():
                print(f"Killing the tmux server at {socket_path}")
                if hasattr(srv, "kill"):
                    srv.kill()
                else:
                    srv.kill_server()
            else:
                print(f"The tmux server at {socket_path} seems to have gone away already")
