from __future__ import annotations

from dataclasses import dataclass

from aqt import mw

from .profiles import DeckProfile, get_profile_repository, resolve_profile


@dataclass(frozen=True)
class DeckReference:
    id: int
    name: str


def deck_references() -> tuple[DeckReference, ...]:
    if mw is None or mw.col is None:
        return ()
    manager = mw.col.decks
    try:
        values = manager.all_names_and_ids()
        references = [DeckReference(int(value.id), str(value.name)) for value in values]
    except (AttributeError, TypeError):
        references = [
            DeckReference(int(value["id"]), str(value["name"]))
            for value in manager.all()
        ]
    return tuple(sorted(references, key=lambda value: value.name.casefold()))


def effective_profile(deck_id: int) -> DeckProfile | None:
    references = deck_references()
    by_id = {reference.id: reference.name for reference in references}
    deck_name = by_id.get(int(deck_id), "")
    if not deck_name:
        return None
    ids_by_name = {reference.name: reference.id for reference in references}
    return resolve_profile(
        get_profile_repository().load(),
        int(deck_id),
        deck_name,
        ids_by_name,
    )
