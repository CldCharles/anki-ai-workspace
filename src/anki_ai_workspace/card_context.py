from __future__ import annotations

from html.parser import HTMLParser
import re

_SOUND_TAG_PATTERN = re.compile(r"\[sound:[^\]]+\]", re.IGNORECASE)
_WHITESPACE_PATTERN = re.compile(r"[ \t\r\f\v]+")
_BLANK_LINES_PATTERN = re.compile(r"\n{3,}")


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in {"br", "div", "p", "li", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"div", "p", "li", "tr"}:
            self.parts.append("\n")


def plain_text(value: str) -> str:
    """Convert an Anki field to readable text while excluding media references."""

    without_sound = _SOUND_TAG_PATTERN.sub("", str(value or ""))
    parser = _TextExtractor()
    parser.feed(without_sound)
    parser.close()
    text = "".join(parser.parts).replace("\xa0", " ")
    text = _WHITESPACE_PATTERN.sub(" ", text)
    text = re.sub(r" *\n *", "\n", text)
    return _BLANK_LINES_PATTERN.sub("\n\n", text).strip()


def context_from_note(note) -> str:
    """Return labeled, non-empty text fields from an Anki note."""

    try:
        fields = note.items()
    except (AttributeError, TypeError):
        return ""

    entries: list[str] = []
    for field_name, value in fields:
        text = plain_text(value)
        if text:
            entries.append(f"{field_name}: {text}")
    return "\n\n".join(entries)


def context_from_card(card) -> str:
    try:
        return context_from_note(card.note())
    except (AttributeError, TypeError):
        return ""


def title_from_card(card, field_name: str = "") -> str:
    """Return a profile-selected title or the first readable note field."""

    try:
        fields = list(card.note().items())
    except (AttributeError, TypeError):
        return ""
    if field_name:
        for name, value in fields:
            if name == field_name:
                selected = plain_text(value)
                if selected:
                    return selected
    return next((plain_text(value) for _name, value in fields if plain_text(value)), "")
