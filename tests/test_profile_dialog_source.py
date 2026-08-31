from __future__ import annotations

from pathlib import Path
import unittest

SOURCE_PATH = (
    Path(__file__).parents[1] / "src" / "anki_ai_workspace" / "profile_dialog.py"
)


class ProfileDialogSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")

    def test_editor_opens_at_a_comfortable_size(self) -> None:
        self.assertIn("self.setMinimumSize(900, 650)", self.source)
        self.assertIn("self.resize(1050, 760)", self.source)

    def test_multiline_prompt_fields_have_room_for_real_prompts(self) -> None:
        self.assertIn("self.profile_context.setMinimumHeight(130)", self.source)
        self.assertIn("self.action_instruction.setMinimumHeight(190)", self.source)
        self.assertIn("self.action_instruction.setMaximumHeight(300)", self.source)
