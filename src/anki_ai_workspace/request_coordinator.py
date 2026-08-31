from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
import threading
from typing import Callable

from .codex_client import CodexResult


@dataclass(frozen=True)
class RequestHandle:
    request_id: int


@dataclass
class ChatRequest:
    handle: RequestHandle
    run: Callable[[threading.Event], CodexResult]
    on_started: Callable[[RequestHandle], None]
    on_finished: Callable[[RequestHandle, CodexResult], None]
    cancelled: threading.Event = field(default_factory=threading.Event)


class ChatRequestCoordinator:
    """A main-thread queue; Anki runs the active request in its task manager."""

    def __init__(self) -> None:
        self._pending: deque[ChatRequest] = deque()
        self._active: ChatRequest | None = None
        self._next_request_id = 1

    def submit(
        self,
        run: Callable[[threading.Event], CodexResult],
        *,
        on_started: Callable[[RequestHandle], None],
        on_finished: Callable[[RequestHandle, CodexResult], None],
    ) -> tuple[RequestHandle, ChatRequest | None]:
        request = ChatRequest(
            handle=RequestHandle(self._next_request_id),
            run=run,
            on_started=on_started,
            on_finished=on_finished,
        )
        self._next_request_id += 1
        self._pending.append(request)
        return request.handle, self._start_next()

    def complete(self, handle: RequestHandle) -> ChatRequest | None:
        if self._active is None or self._active.handle != handle:
            return None
        self._active = None
        return self._start_next()

    def cancel(self, handle: RequestHandle) -> ChatRequest | None:
        """Signal an active request or return a queued request for UI completion."""

        if self._active is not None and self._active.handle == handle:
            self._active.cancelled.set()
            return None
        for request in tuple(self._pending):
            if request.handle == handle:
                self._pending.remove(request)
                request.cancelled.set()
                return request
        return None

    def _start_next(self) -> ChatRequest | None:
        if self._active is not None or not self._pending:
            return None
        self._active = self._pending.popleft()
        return self._active
