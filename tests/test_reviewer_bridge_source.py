from __future__ import annotations

import unittest
from pathlib import Path

SOURCE_PATH = (
    Path(__file__).parents[1]
    / "src"
    / "anki_ai_workspace"
    / "web"
    / "reviewer_bridge.js"
)


class ReviewerBridgeSourceTests(unittest.TestCase):
    def test_bridge_activates_each_new_card_client_once(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")

        self.assertIn("source.dataset.ankiAIWorkspaceActivated", source)
        self.assertIn("document.head.appendChild(client)", source)
        self.assertIn("new MutationObserver(activateCurrentCard)", source)
        self.assertNotIn("observer.disconnect()", source)
        self.assertIn("Keep observing", source)
        self.assertIn("observer.observe(document.documentElement", source)
        self.assertIn("__ankiAIWorkspaceReviewerBridgeInstalled", source)
