from __future__ import annotations

import unittest

from anki_ai_workspace.codex_client import CodexResult
from anki_ai_workspace.request_coordinator import ChatRequestCoordinator


class RequestCoordinatorTests(unittest.TestCase):
    def test_only_one_request_is_active_and_next_starts_on_completion(self) -> None:
        coordinator = ChatRequestCoordinator()
        first_handle, first = coordinator.submit(
            lambda _cancelled: CodexResult(text="first"),
            on_started=lambda _handle: None,
            on_finished=lambda *_: None,
        )
        second_handle, second = coordinator.submit(
            lambda _cancelled: CodexResult(text="second"),
            on_started=lambda _handle: None,
            on_finished=lambda *_: None,
        )

        self.assertIsNotNone(first)
        self.assertIsNone(second)
        self.assertEqual(first.handle, first_handle)
        next_request = coordinator.complete(first_handle)
        self.assertIsNotNone(next_request)
        self.assertEqual(next_request.handle, second_handle)

    def test_cancelling_queued_request_removes_it_without_touching_active_work(
        self,
    ) -> None:
        coordinator = ChatRequestCoordinator()
        first_handle, _first = coordinator.submit(
            lambda _cancelled: CodexResult(text="first"),
            on_started=lambda _handle: None,
            on_finished=lambda *_: None,
        )
        second_handle, _second = coordinator.submit(
            lambda _cancelled: CodexResult(text="second"),
            on_started=lambda _handle: None,
            on_finished=lambda *_: None,
        )

        cancelled = coordinator.cancel(second_handle)

        self.assertIsNotNone(cancelled)
        self.assertTrue(cancelled.cancelled.is_set())
        self.assertIsNone(coordinator.complete(first_handle))

    def test_cancelling_active_request_signals_its_process_event(self) -> None:
        coordinator = ChatRequestCoordinator()
        handle, request = coordinator.submit(
            lambda _cancelled: CodexResult(text="first"),
            on_started=lambda _handle: None,
            on_finished=lambda *_: None,
        )

        cancelled = coordinator.cancel(handle)

        self.assertIsNone(cancelled)
        self.assertIsNotNone(request)
        self.assertTrue(request.cancelled.is_set())
