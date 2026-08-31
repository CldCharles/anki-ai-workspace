import unittest

from anki_ai_workspace.card_context import (
    context_from_note,
    plain_text,
    title_from_card,
)


class FakeNote:
    def items(self):
        return [
            ("Front", "<b>Earth</b><br>행성"),
            ("Audio", "[sound:earth.mp3]"),
            ("Image", '<img src="earth.png">'),
            ("Back", "A planet."),
        ]


class FakeCard:
    def note(self):
        return FakeNote()


class CardContextTests(unittest.TestCase):
    def test_plain_text_removes_html_and_sound_tags(self) -> None:
        self.assertEqual(
            plain_text("<div>Hello<br>world</div>[sound:x.mp3]"), "Hello\nworld"
        )

    def test_context_contains_only_non_empty_text_fields(self) -> None:
        context = context_from_note(FakeNote())

        self.assertEqual(context, "Front: Earth\n행성\n\nBack: A planet.")

    def test_title_prefers_configured_field_then_first_readable_field(self) -> None:
        card = FakeCard()
        self.assertEqual(title_from_card(card, "Back"), "A planet.")
        self.assertEqual(title_from_card(card, "Missing"), "Earth\n행성")
        self.assertEqual(title_from_card(card, "Audio"), "Earth\n행성")
