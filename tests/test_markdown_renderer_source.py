from __future__ import annotations

import unittest

from anki_ai_workspace.markdown_renderer import MARKDOWN_RENDERER_SCRIPT


class MarkdownRendererSourceTests(unittest.TestCase):
    def test_supports_requested_markdown_blocks_and_inline_formatting(self) -> None:
        for feature in (
            "<strong>$1</strong>",
            "<em>$2</em>",
            "<pre><code>",
            "<blockquote>",
            "<table>",
            "<h${level}>",
        ):
            self.assertIn(feature, MARKDOWN_RENDERER_SCRIPT)

    def test_escapes_raw_html_before_rendering_markdown(self) -> None:
        self.assertIn("const escapeHtml", MARKDOWN_RENDERER_SCRIPT)
        self.assertIn("let text=escapeHtml(value)", MARKDOWN_RENDERER_SCRIPT)
        self.assertIn("escapeHtml(content.join", MARKDOWN_RENDERER_SCRIPT)

    def test_renderer_can_be_loaded_for_multiple_reviewer_cards(self) -> None:
        self.assertIn("window.AnkiAIWorkspaceMarkdown=", MARKDOWN_RENDERER_SCRIPT)
        self.assertNotIn("const AnkiAIWorkspaceMarkdown=", MARKDOWN_RENDERER_SCRIPT)

    def test_allows_only_web_or_mailto_links(self) -> None:
        self.assertIn("/^(https?:\\/\\/|mailto:)[^\\s]+$/i", MARKDOWN_RENDERER_SCRIPT)
        self.assertIn('target="_blank"', MARKDOWN_RENDERER_SCRIPT)
        self.assertIn('rel="noopener noreferrer"', MARKDOWN_RENDERER_SCRIPT)
