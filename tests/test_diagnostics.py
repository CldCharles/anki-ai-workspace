from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from anki_ai_workspace.diagnostics import LOG_FILENAME, configure_log, logger


class DiagnosticsTests(unittest.TestCase):
    def test_log_is_created_under_anki_logs_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = configure_log(temporary_directory)
            logger().info("task submitted request_id=1")

            self.assertEqual(path.name, LOG_FILENAME)
            self.assertEqual(path.parent.name, "logs")
            self.assertIn("request_id=1", path.read_text(encoding="utf-8"))
